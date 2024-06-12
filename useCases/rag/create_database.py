from tool_pdf import extract_text_from_pdf
from chunking import semantic_chunking
from embed import Embedding
import numpy as np

if __name__ == "__main__":
    pdf_path = "1.pdf"  # 替换为你的PDF文件路径
    pdf_text = extract_text_from_pdf(pdf_path)
    #print(pdf_text)

    sentences=pdf_text.splitlines()
    sentence_embeddings=Embedding("text-embedding-3-small")
    chunks = semantic_chunking(sentences, sentence_embeddings)
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}:")
        for sentence in chunk:
            print(f"  {sentence}")