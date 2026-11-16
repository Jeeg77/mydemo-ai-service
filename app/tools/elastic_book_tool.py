import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from langchain.tools import tool, ToolRuntime
from app.models.elastic_book_state import ElasticBookState

# Load environment variables from .env file
load_dotenv()

es = Elasticsearch(
    os.getenv("ELASTICSEARCH_HOST"),
    basic_auth=(os.getenv("ELASTICSEARCH_USERNAME"), os.getenv("ELASTICSEARCH_PASSWORD"))
)

@tool("search_books", return_direct=True)
def search_books(
    runtime: ToolRuntime[None, ElasticBookState],
    size: int = 5
):
    
    """
    Search for books in the internal catalog using Elasticsearch.
    """
    print("STATO RICEVUTO DAL TOOL:", runtime.state)


    title = runtime.state["title"]
    author = runtime.state["author"]
    year = runtime.state["year"]

    
    print("\n========== SEARCH BOOKS ==========")
    print(f"Titolo: {title}")
    print(f"Autore: {author}")
    print(f"Anno: {year}")
    print(f"Size: {size}")

    filters = []

    if title and title.lower() != "tutti i titoli":
        filters.append({
            "match": {
                "title": title
            }
        })

    if author and author.lower() != "tutti gli autori":
        filters.append({
            "match": {
                "author": author
            }
        })

    if year is not None and str(year).isdigit():
        filters.append({
            "term": {
                "year": int(year)
            }
        })

    if not filters:
        return []

    response = es.search(
        index="books",
        body={
            "query": {
                "bool": {
                    "must": filters
                }
            },
            "size": size
        }
    )

    print(f"Risposta Elasticsearch: {response}")
    print("==================================\n")

    results = []

    for hit in response["hits"]["hits"]:
        source = hit["_source"]

        results.append({
            "title": source.get("title"),
            "author": source.get("author"),
            "publication_year": source.get("year"),
            "description": source.get("description"),
            "id": hit["_id"]
        })

    return results


def get_elastic_tools():
    return [search_books]

"""
def test_search_dostoevskij():
    response = es.search(
        index="books",
        query={
            "term": {
                "author": "Fedor Michajlovic Dostoevskij"
            }
        }
    )

    print("\n========== TEST DIRETTO ELASTIC ==========")
    print(response["hits"]["total"])

    for hit in response["hits"]["hits"]:
        print(hit["_source"])

    print("==========================================")
"""
