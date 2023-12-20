from dotenv import load_dotenv
import os
import chromadb
from llama_index.llms import AzureOpenAI
from llama_index.embeddings import AzureOpenAIEmbedding
from llama_index import VectorStoreIndex, ServiceContext

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from llama_index import set_global_service_context
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
from llama_index.schema import Document

from bs4 import BeautifulSoup

proxies = {"http": "socks5h://localhost:9050", "https": "socks5h://localhost:9050"}

headers = {"User-Agent": "Mozilla/5.0"}

load_dotenv()


api_key = os.getenv("AZURE_CHATGPT_API_KEY")
azure_endpoint = os.getenv("AZURE_CHATGPT_ENDPOINT")

api_version = "2023-07-01-preview"

embed_model = AzureOpenAIEmbedding(
    model="text-embedding-ada-002",
    deployment_name="text-embedding-ada-002",
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version,
)

llm = AzureOpenAI(
    model="gpt-35-turbo",
    deployment_name="gpt-35-turbo",
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version,
)

service_context = ServiceContext.from_defaults(
    llm=llm,
    embed_model=embed_model,
)

set_global_service_context(service_context)

def create_embedding_store(name):
    chroma_client = chromadb.Client()
    return chroma_client.create_collection(name)
global collection

collection = create_embedding_store("supertype")

vector_store = ChromaVectorStore(chroma_collection=collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)


def query_pages(collection, url, questions):
    with open("darkweb_2.html", "r") as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    docs = soup.get_text()
    docs = [Document(text=docs)]


    index = VectorStoreIndex.from_documents(docs, storage_context=storage_context)

    query_engine = index.as_query_engine()

    answer = query_engine.query(questions)
    if hasattr(answer, 'response'):
        extracted_response = answer.response

    return extracted_response

def main():
    ai_query = 'Assume the role of cyber police and aid in identifying a potential culprit based on the provided content. Extract valuable information in a list of JSON format, with each object adhering to the structure {"username": "", "significance": "", "date": "", "addresses": [], "category": "", "other_info": ""}. The date should follow the format dd/mm/yyyy. In the JSON structure, significance provides a concise description of the post\'s context, and the category can be one of the following: drugs, weapons, porn, or other. The addresses field comprises cryptocurrency addresses mentioned in the post. Provide only the final JSON list as the output, with one JSON object for each post. (for each and evry post) (don\'t miss any post)'


    answers = query_pages(collection, ai_query)
    print(answers)

    return (answers)

main()