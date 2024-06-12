from elasticsearch import Elasticsearch, helpers, exceptions
from urllib.request import urlopen
from getpass import getpass
import json
import time
import openai
from pinecone_datasets import load_dataset
import os
from pinecone import Pinecone
from pinecone import ServerlessSpec
class Search_rag:
    """
    given the embedding of query, search for relevant docs with score

    input:the embedding of query------list[float]
    output:related documents with score
    """
    def __init__(self,query,documents,embedding_model):
        self.query=query
        self.documents=documents
        self.embedding_model=embedding_model


    def keyword_search(self):
        query_keywords = set(self.query.lower().split())
        doc_scores = []

        for doc in self.documents:
            doc_keywords = set(doc.lower().split())
            score = len(query_keywords & doc_keywords)
            doc_scores.append((score, doc))

        doc_scores.sort(reverse=True, key=lambda x: x[0])
        return [doc for score, doc in doc_scores if score > 0]


    def elastic_search(self):
        # https://www.elastic.co/search-labs/tutorials/install-elasticsearch/elastic-cloud#finding-your-cloud-id
        ELASTIC_CLOUD_ID = getpass("Elastic Cloud ID: ")

        # https://www.elastic.co/search-labs/tutorials/install-elasticsearch/elastic-cloud#creating-an-api-key
        ELASTIC_API_KEY = getpass("Elastic Api Key: ")

        # Create the client instance
        client = Elasticsearch(
            # For local development
            # hosts=["http://localhost:9200"]
            cloud_id=ELASTIC_CLOUD_ID,
            api_key=ELASTIC_API_KEY,
        )

        API_KEY = getpass("OpenAI API key: ")

        client.inference.put_model(
            task_type="text_embedding",
            inference_id="my_openai_embedding_model",
            body={
                "service": "openai",
                "service_settings": {"api_key": API_KEY},
                "task_settings": {"model": self.embedding_model},
            },
        )

        client.ingest.put_pipeline(
            id="openai_embeddings_pipeline",
            description="Ingest pipeline for OpenAI inference.",
            processors=[
                {
                    "inference": {
                        "model_id": "my_openai_embedding_model",
                        "input_output": {
                            "input_field": "plot",
                            "output_field": "plot_embedding",
                        },
                    }
                }
            ],
        )

        client.indices.delete(index="openai-movie-embeddings", ignore_unavailable=True)
        client.indices.create(
            index="openai-movie-embeddings",
            settings={"index": {"default_pipeline": "openai_embeddings_pipeline"}},
            mappings={
                "properties": {
                    "plot_embedding": {
                        "type": "dense_vector",
                        "dims": 1536,
                        "similarity": "dot_product",
                    },
                    "plot": {"type": "text"},
                }
            },
        )


        #后续，针对elastic search的数据格式要封装出来
        url = "https://raw.githubusercontent.com/elastic/elasticsearch-labs/main/notebooks/search/movies.json"
        response = urlopen(url)

        # Load the response data into a JSON object
        data_json = json.loads(response.read())

        # Prepare the documents to be indexed
        documents = []
        for doc in data_json:
            documents.append(
                {
                    "_index": "openai-movie-embeddings",
                    "_source": doc,
                }
            )

        # Use helpers.bulk to index
        helpers.bulk(client, documents)

        print("Done indexing documents into `openai-movie-embeddings` index!")
        time.sleep(3)

        response = client.search(
            index="openai-movie-embeddings",
            size=3,
            knn={
                "field": "plot_embedding",
                "query_vector_builder": {
                    "text_embedding": {
                        "model_id": "my_openai_embedding_model",
                        "model_text": "Fighting movie",
                    }
                },
                "k": 10,
                "num_candidates": 100,
            },
        )

        docs_with_score=[]
        for hit in response["hits"]["hits"]:
            doc_id = hit["_id"]
            score = hit["_score"]
            title = hit["_source"]["title"]
            plot = hit["_source"]["plot"]
            docs_with_score.append((score,plot))
            print(f"Score: {score}\nTitle: {title}\nPlot: {plot}\n")

        return docs_with_score

    def search_pinecone(self):
        dataset = load_dataset('youtube-transcripts-text-embedding-ada-002')
        # we drop sparse_values as they are not needed for this example
        dataset.documents.drop(['metadata'], axis=1, inplace=True)
        dataset.documents.rename(columns={'blob': 'metadata'}, inplace=True)
        dataset.head()

        # initialize connection to pinecone (get API key at app.pinecone.io)
        api_key = os.environ.get('PINECONE_API_KEY') or 'PINECONE_API_KEY'

        # configure client
        pc = Pinecone(api_key=api_key)

        cloud = os.environ.get('PINECONE_CLOUD') or 'aws'
        region = os.environ.get('PINECONE_REGION') or 'us-east-1'

        spec = ServerlessSpec(cloud=cloud, region=region)

        index_name = 'gen-qa-openai-fast'

        # check if index already exists (it shouldn't if this is first time)
        if index_name not in pc.list_indexes().names():
            # if does not exist, create index
            pc.create_index(
                index_name,
                dimension=1536,  # dimensionality of text-embedding-ada-002
                metric='cosine',
                spec=spec
            )
        # connect to index
        index = pc.Index(index_name)
        # view index stats
        index.describe_index_stats()

        for batch in dataset.iter_documents(batch_size=100):
            index.upsert(batch)

        # get api key from platform.openai.com
        openai.api_key = os.getenv('OPENAI_API_KEY') or 'sk-...'

        embed_model = self.embedding_model

        query = (
                "Which training method should I use for sentence transformers when " +
                "I only have pairs of related sentences?"
        )

        res = openai.Embedding.create(
            input=[query],
            engine=embed_model
        )

        # retrieve from Pinecone
        xq = res['data'][0]['embedding']

        # get relevant contexts (including the questions)
        res = index.query(vector=xq, top_k=2, include_metadata=True)




