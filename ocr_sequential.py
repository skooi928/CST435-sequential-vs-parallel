# Import necessary library
import pytesseract
import time
import pymupdf
from PIL import Image

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

# Record the start time of the OCR process
start_time = time.time()

print("Starting OCR process at ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time)))
# For loop for sequential OCR processing of each page
for page_number in range(total_pages):
    # Perform OCR on the image
    extracted_text += process_page(page_number)
    
end_time = time.time()

# Calculate the total time taken for the OCR process
time_taken = end_time - start_time
print("Ending OCR process at ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time)))
print(f"OCR process completed in {time_taken:.2f} seconds.")
    
# Save the extracted text to a file
with open("Result/extracted_text_sequential.txt", "w", encoding="utf-8") as text_file:
    text_file.write(extracted_text)