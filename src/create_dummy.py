import argparse
import os
from pdf_utils import create_dummy_pdf

def main():
    parser = argparse.ArgumentParser(description="Create a dummy PDF by sampling pages from a source PDF.")
    parser.add_argument("source_pdf", help="Path to the source PDF file.")
    parser.add_argument("output_pdf", help="Path to the output dummy PDF file.")
    parser.add_argument("--pages", type=int, default=10, help="Number of pages to sample.")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.source_pdf):
        print(f"Error: Source PDF {args.source_pdf} not found.")
        return
        
    create_dummy_pdf(args.source_pdf, args.output_pdf, args.pages)

if __name__ == "__main__":
    main()
