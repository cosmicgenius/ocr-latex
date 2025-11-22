HEADER_PROMPT = """
You are an expert LaTeX typesetter. 
I will provide you with several images of pages from a mathematics book. These pages are not guaranteed to be consecutive.
Your task is to generate a single LaTeX header that can be used to typeset these pages.

The header should include:
1. The `\\documentclass` (e.g., book, article) with appropriate options.
2. Necessary packages (e.g., amsmath, amssymb, tikz, etc.) based on the symbols and diagrams you see.
3. Custom macros or environments that seem to be used consistently (e.g., for theorems, definitions, lemmas, proofs).
4. Anything required to typeset page headers and footers (e.g. page numbers).
5. A special macro called \\REF that passes through the reference number. I want this so that I can grep for these references in the future.
   In addition, to make this work, please enforce that environments must be manually numbered.
6. If you receive the cover, just use your best effort.

Do NOT transcribe the content of the pages. 
Output ONLY the LaTeX preamble/header code. 
Start with `\\documentclass` and end before `\\begin{document}`.
"""

TRANSCRIPTION_PROMPT = """
You are an expert LaTeX typesetter.
I will provide you with an image of a page from a mathematics book.
I will also provide the LaTeX header that should be used for this document.

Your task is to transcribe the CONTENT of this page into LaTeX code.

Rules:
1. Use the macros and environments defined in the header where appropriate.
2. There is a special macro called \\REF that passes through the reference number. I want this so that I can grep for these references in the future.
   Please use this macro for all references. In addition, please manually number every environment.
3. Do NOT include the header, `\\documentclass`, or `\\begin{{document}}`.
4. Do NOT include `\\end{{document}}`.
5. Output ONLY the LaTeX code for the body of this page.
6. If there are figures, try to describe them in TikZ or use a placeholder if too complex, but prefer transcribing text and math formulas accurately.
7. Pay close attention to mathematical notation.
8. If you receive the cover, just use your best effort.

Here is the header for context:
```latex
{header}
```
"""
