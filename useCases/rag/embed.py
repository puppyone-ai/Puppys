import os
from openai import OpenAI

api_key=os.environ.get("OPENAI_API_KEY")
client=OpenAI(api_key=api_key)

texts=["you are my sunshine!","it is my life"]
#get the embedding list of a list of strings


class Embedding:
    def __init__(self,embed_model):
        self.embed_model=embed_model

    def get_embeddings(self,texts: list[str]) -> list[list[float]]:
        texts = [i.replace("\n", " ") for i in texts]
        embed = client.embeddings.create(input=texts, model=self.embed_model).data
        embedding_list = []
        for i in embed:
            embedding_list.append(i.embedding)
        return embedding_list


if __name__ == "__main__":
    Embed=Embedding("text-embedding-3-small")
    embed=Embed.get_embeddings(texts)
    for i in embed:
        print(i)
        print("\n")