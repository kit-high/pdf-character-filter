import fitz 
import sys
import matplotlib.pyplot as plt
from tqdm import tqdm

def remove_small_text(input_pdf, output_pdf, font_size_threshold):
    doc = fitz.open(input_pdf)
    sizes = []

    for page_num in tqdm(range(doc.page_count), desc="Processing pages"):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        try:                            
                            sizes.append(span["size"])

                            if span["size"] <= font_size_threshold:
                                rect = fitz.Rect(span["bbox"])
                                page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
                        except Exception as e:
                            print(f"Error processing span: {e}")

    doc.save(output_pdf)

    plt.hist(sizes, bins=30, edgecolor='black')
    plt.title('Distribution of Font Sizes')
    plt.xlabel('Font Size')
    plt.xlim(0,15)
    plt.ylabel('Frequency')
    plt.savefig('font_size_hist.png')

input_pdf = sys.argv[1]
output_pdf = sys.argv[2]
font_size_threshold = sys.argv[3]
remove_small_text(input_pdf, output_pdf, font_size_threshold)