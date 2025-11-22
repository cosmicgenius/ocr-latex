import os
import argparse
from dotenv import load_dotenv
from pdf_utils import sample_random_pages, convert_pdf_to_images
from ocr_utils import generate_latex_header, transcribe_page
from google import genai

def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="OCR a PDF to LaTeX using Gemini.")
    parser.add_argument("pdf_path", nargs="?", default="Altman_Kleiman_Commutative_Algebra.pdf", help="Path to the PDF file.")
    parser.add_argument("--output", default="output.tex", help="Output LaTeX file.")
    parser.add_argument("--sample-k", type=int, default=10, help="Number of pages to sample for header generation.")
    parser.add_argument("--model", default="gemini-2.5-flash", help="Gemini model to use.")
    
    args = parser.parse_args()
    
    pdf_path = args.pdf_path
    
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file {pdf_path} not found.")
        return

    print(f"Processing {pdf_path}...")

    # Automatically loads API key from the environment variable `GEMINI_API_KEY`.
    client = genai.Client()

    # Step 1: Generate Header
    print(f"Sampling {args.sample_k} pages for header generation...")
    sample_images = sample_random_pages(pdf_path, k=args.sample_k)
    
    print("Generating LaTeX header...")
    try:
        header = generate_latex_header(client, args.model, sample_images)
    except Exception as e:
        print(f"Error generating header: {e}")
        return
        
    print("Header generated.")
    print("-" * 20)
    print(header)
    print("-" * 20)

    # Step 2: Transcribe Pages
    print("Converting all pages to images for transcription...")
    all_images = convert_pdf_to_images(pdf_path)
    
    full_latex_content = []
    
    # Clean up the header (remove markdown code blocks if present)
    clean_header = header.replace("```latex", "").replace("```", "").strip()
    
    full_latex_content.append(clean_header)
    full_latex_content.append("\\begin{document}")
    
    print(f"Transcribing {len(all_images)} pages...")
    for i, img in enumerate(all_images):
        print(f"Transcribing page {i+1}/{len(all_images)}...")
        try:
            page_content = transcribe_page(client, args.model, img, clean_header)
            
            # Clean up page content
            clean_page_content = page_content.replace("```latex", "").replace("```", "").strip()
            
            full_latex_content.append(f"% Page {i+1}")
            full_latex_content.append(clean_page_content)
            full_latex_content.append("\\newpage")
        except Exception as e:
            print(f"Error transcribing page {i+1}: {e}")
            full_latex_content.append(f"% Error transcribing page {i+1}")

    full_latex_content.append("\\end{document}")
    
    # Save to file
    with open(args.output, "w") as f:
        f.write("\n\n".join(full_latex_content))
        
    print(f"Done! Output saved to {args.output}")

if __name__ == "__main__":
    main()
