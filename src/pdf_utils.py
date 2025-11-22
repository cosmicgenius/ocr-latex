import random
from pathlib import Path
from typing import List, Generator
from pdf2image import convert_from_path
from pypdf import PdfReader, PdfWriter
from PIL import Image

def convert_pdf_to_images(pdf_path: str) -> List[Image.Image]:
    """
    Convert a PDF file to a list of PIL images.
    """
    return convert_from_path(pdf_path)

def sample_random_pages(pdf_path: str, k: int = 10) -> List[Image.Image]:
    """
    Sample k random pages from the PDF and return them as images.
    """
    reader = PdfReader(pdf_path)
    num_pages = len(reader.pages)
    
    if num_pages <= k:
        # If fewer pages than k, return all pages
        indices = list(range(num_pages))
    else:
        indices = sorted(random.sample(range(num_pages), k))
    
    # We can't easily convert specific pages efficiently with pdf2image without converting the whole thing 
    # or using first_page/last_page in a loop. 
    # For efficiency with pdf2image, it's better to extract the pages to a temporary PDF or just use the indices.
    # Let's use the first_page/last_page argument of convert_from_path in a loop for the sampled indices.
    
    images = []
    for i in indices:
        # pdf2image uses 1-based indexing for first_page/last_page
        page_images = convert_from_path(pdf_path, first_page=i+1, last_page=i+1)
        if page_images:
            images.append(page_images[0])
            
    return images

def create_dummy_pdf(source_path: str, output_path: str, num_pages: int = 10):
    """
    Create a dummy PDF by randomly sampling pages from the source PDF.
    """
    reader = PdfReader(source_path)
    writer = PdfWriter()
    
    total_pages = len(reader.pages)
    if total_pages <= num_pages:
        indices = range(total_pages)
    else:
        indices = sorted(random.sample(range(total_pages), num_pages))
        
    for i in indices:
        writer.add_page(reader.pages[i])
        
    with open(output_path, "wb") as f:
        writer.write(f)
    
    print(f"Created dummy PDF at {output_path} with {len(indices)} pages.")
