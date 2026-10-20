# Import necessary library
import pytesseract
import os
from concurrent.futures import ThreadPoolExecutor
import time
import pymupdf
from PIL import Image

# Record the start time of the OCR process
start_time = time.time()

# Initialize the path to the Tesseract OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Initialize the pdf file path
pdf_path = "411pages_report.pdf"

# Initialize an empty string to store the extracted text
extracted_text = ""

# Get the page counts for the for loop count
with pymupdf.open(pdf_path) as doc:
    total_pages = doc.page_count

# Define a function to perform OCR on a single page
def process_page(page_number):
    # Convert the specific page to an image
    with pymupdf.open(pdf_path) as doc:
        page = doc.load_page(page_number)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    # Perform OCR on the image
    return pytesseract.image_to_string(img)

# Use ThreadPoolExecutor to process pages in parallel
# Define worker number based on the number of available CPU cores
max_workers = os.cpu_count()  # Get the number of available CPU cores
page_numbers = list(range(total_pages))
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    # Map the process_page function to the page numbers
    single_page_extraction_text = list(executor.map(process_page, page_numbers))
# Combine the results in order into a single string
extracted_text = '/n'.join(single_page_extraction_text)
    
# Save the extracted text to a file
with open("Result/extracted_text_parallel.txt", "w", encoding="utf-8") as text_file:
    text_file.write(extracted_text)

end_time = time.time()

# Calculate the total time taken for the OCR process
time_taken = end_time - start_time
print(f"OCR process completed in {time_taken:.2f} seconds.")