import os
from google import genai
from PIL import Image
from typing import List
from prompts import HEADER_PROMPT, TRANSCRIPTION_PROMPT

def generate_latex_header(
    client: genai.Client,
    model: str,
    images: List[Image.Image]
) -> str:
    """
    Generates a LaTeX header (documentclass, packages, macros) based on a sample of pages.
    """
    # Gemini accepts a list of parts (text + images)
    content = [HEADER_PROMPT] + images
    
    response = client.models.generate_content(
        model=model,
        contents=content
    )
    return response.text

def transcribe_page(
    client: genai.Client,
    model: str,
    image: Image.Image,
    header: str
) -> str:
    """
    Transcribes a single page image to LaTeX content, using the provided header as context.
    """
    
    prompt = TRANSCRIPTION_PROMPT.format(header=header)
    content = [prompt, image]
    
    response = client.models.generate_content(
        model=model,
        contents=content
    )
    return response.text
