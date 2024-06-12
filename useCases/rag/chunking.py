from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def semantic_chunking(sentences, embeddings, threshold=0.75):
    chunks = []
    current_chunk = []
    current_embeddings = []

    for i, (sentence, embedding) in enumerate(zip(sentences, embeddings)):
        if not current_chunk:
            current_chunk.append(sentence)
            current_embeddings.append(embedding)
            continue

        similarities = cosine_similarity([embedding], current_embeddings)
        max_similarity = np.max(similarities)

        if max_similarity < threshold:
            chunks.append(current_chunk)
            current_chunk = [sentence]
            current_embeddings = [embedding]
        else:
            current_chunk.append(sentence)
            current_embeddings.append(embedding)

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

sentences=[]
sentence_embeddings=[]
if __name__ == "__main__":
    chunks = semantic_chunking(sentences, sentence_embeddings.numpy())
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}:")
        for sentence in chunk:
            print(f"  {sentence}")