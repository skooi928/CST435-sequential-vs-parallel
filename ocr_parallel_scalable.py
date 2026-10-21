import csv
import os
import time
from concurrent.futures import ThreadPoolExecutor

import pymupdf
import pytesseract
from PIL import Image


TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
PDF_PATH = "411pages_report.pdf"
RESULT_DIRECTORY = "Result"
TIMING_FILE = os.path.join(RESULT_DIRECTORY, "ocr_thread_timings.csv")


pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def process_page(page_number: int) -> str:
    """Render one PDF page and perform OCR on it."""
    with pymupdf.open(PDF_PATH) as document:
        page = document.load_page(page_number)
        pixmap = page.get_pixmap()
        image = Image.frombytes(
            "RGB",
            [pixmap.width, pixmap.height],
            pixmap.samples,
        )

    return pytesseract.image_to_string(image)


def run_ocr(thread_count: int, page_numbers: list[int]) -> float:
    """Run OCR using the requested number of worker threads."""
    start_time = time.perf_counter()

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        page_text = list(executor.map(process_page, page_numbers))

    extracted_text = "\n".join(page_text)

    end_time = time.perf_counter()

    output_file = os.path.join(
        RESULT_DIRECTORY,
        f"extracted_text_{thread_count}_threads.txt",
    )

    with open(output_file, "w", encoding="utf-8") as text_file:
        text_file.write(extracted_text)

    return end_time - start_time


def main() -> None:
    os.makedirs(RESULT_DIRECTORY, exist_ok=True)

    with pymupdf.open(PDF_PATH) as document:
        total_pages = document.page_count

    page_numbers = list(range(total_pages))
    timing_results: list[dict[str, object]] = []

    print(f"Total pages: {total_pages}")
    print("Starting OCR benchmark...\n")

    for thread_count in range(1, 9):
        print(f"Running OCR with {thread_count} thread(s)...")

        elapsed_time = run_ocr(thread_count, page_numbers)

        timing_results.append(
            {
                "thread_count": thread_count,
                "time_seconds": round(elapsed_time, 2),
            }
        )

        print(
            f"Completed with {thread_count} thread(s): "
            f"{elapsed_time:.2f} seconds\n"
        )

    with open(TIMING_FILE, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=["thread_count", "time_seconds"],
        )
        writer.writeheader()
        writer.writerows(timing_results)

    print(f"Timing results saved to: {TIMING_FILE}")


if __name__ == "__main__":
    main()