import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):

    pdf_document = fitz.open(pdf_path)
    text = ""

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)

        page_text = page.get_text()
        text += page_text

    return text


if __name__ == "__main__":
    pdf_path = "deepseek.pdf"  # 替换为你的PDF文件路径
    pdf_text = extract_text_from_pdf(pdf_path)
    print(pdf_text)
