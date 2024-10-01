import os
import openai
from pymongo import MongoClient
import json
from pymongoarrow.api import write
import pyarrow as pa
import pandas as pd
import numpy as np
from dotenv import load_dotenv

load_dotenv()

def get_embedding(text):
    return openai.Embedding.create(
        input=text,
        model=os.getenv("EMBEDDING_MODEL")
    )['data'][0]['embedding']

client = MongoClient(os.getenv("ATLAS_URI"))

db = client['mystorytime']
collection = db['stories']

document = {"name": "Lili", "city": "Zilina"}
inserted_document = collection.insert_one(document)

print(f"Inserted Document ID: {inserted_document.inserted_id}")

# Query for documents with a specific city
query = {"city": "Sabinov"}
documents = collection.find(query)

for document in documents:
    # Extract the name field from each document
    retrieved_vector = document["name"]
    print(retrieved_vector)

print(retrieved_vector)
client.close()


# query = "imaginary characters from outer space at war"
#
# results = collection.aggregate([
#     {"$vectorSearch": {
#         "queryVector": generate_embedding(query),
#         "path": "plot_embedding_hf",
#         "numCandidates": 100,
#         "limit": 5,
#         "index": "PlotSemanticSearch",
#     }}
# ]);
#
# print(f"{results}")
#
# for document in results:
#     print("AAA")
#     print(f'Movie Name: {document["title"]},\nMovie Plot: {document["plot"]}\n')
#
# print(f"{results}")
