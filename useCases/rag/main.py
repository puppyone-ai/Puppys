import re
import os
from puppy.llm.openAI import open_ai_chat
from openai import OpenAI
import cohere

from rag_decision import rag_decision
from answer_direct import answer_direct
from query_transform import query_transformation
from tokenize import TikTokenizer
from embed import Embedding
from Search_rag import Search_rag
from utils import remove_duplicates
from generate import Generate

os.environ["OPENAI_API_KEY"]="sk-proj-5uTAMBmeOUnf44LUVpNnT3BlbkFJXqxG7FaQGUYCHOpT7j8p"
class Rag_decisionError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)
def rag_decisiontree(query):

    rag_or_not=rag_decision(query)

    rag_or_not="Yes"
    if rag_or_not=="Yes":
        multi_q=query_transformation(query,5)
        chunk_list=[]
        for q in multi_q:

            #tokenizer = TikTokenizer()
            #tokens = tokenizer.tokenize("This is an example sentence.")

            api_key = os.environ.get("OPENAI_API_KEY")
            client = OpenAI(api_key=api_key)

            Embed = Embedding("text-embedding-3-small")
            embedding = Embedding.get_embeddings(q)

            retriver=Search_rag()
            chunk=retriver.search_pinecone()
            chunk_list.append(chunk)

        unique_chunklist=remove_duplicates(chunk_list)
        co = cohere.Client("<<apiKey>>")
        response = co.rerank(
            model="rerank-english-v3.0",
            query="What is the capital of the United States?",
            documents=unique_chunklist,
            top_n=3,
        )

        Generate(response)

    elif rag_or_not=="No":
        answer_direct(query)
    else:
        raise Rag_decisionError("the output of llm is wrong!\n")

if __name__ == "__main__":
    rag_decisiontree("which is the best university in the China?")



