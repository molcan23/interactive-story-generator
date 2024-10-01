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

def insert_user_item(client, db_name, collection_name, user_id, story_id, summary):
    """Inserts a user-item document into a specified MongoDB collection.

    Args:
        client (MongoClient): A MongoClient instance connected to the MongoDB database.
        db_name (str): The name of the database.
        collection_name (str): The name of the collection.
        user_id (str): The user ID.
        story_id (str): The story ID.
        summary (str): The summary of the user-item.

    Returns:
        ObjectId: The ObjectId of the inserted document.
    """

    db = client[db_name]
    collection = db[collection_name]
    document = {"user_id": user_id, "story_id": story_id, "summary": summary}
    inserted_document = collection.insert_one(document)
    return inserted_document.inserted_id

def query_user_items(client, db_name, collection_name, query):
    """Queries a MongoDB collection for user-items based on a specified query.

    Args:
        client (MongoClient): A MongoClient instance connected to the MongoDB database.
        db_name (str): The name of the database.
        collection_name (str): The name of the collection.
        query (dict): The query criteria.

    Returns:
        list: A list of user-item documents matching the query.
    """

    db = client[db_name]
    collection = db[collection_name]
    documents = collection.find(query)
    return list(documents)

def extract_field(document, field_name):
    """Extracts a specified field from a document.

    Args:
        document (dict): The document.
        field_name (str): The name of the field to extract.

    Returns:
        Any: The value of the field, or None if the field doesn't exist.
    """

    return document.get(field_name)

# Connect to MongoDB
client = MongoClient(os.getenv("ATLAS_URI"))

# Insert a user-item
user_id = "user123"
story_id = "story456"
summary = "This is a summary of the story."
user_item_id = insert_user_item(client, "mystorytime", "user_items", user_id, story_id, summary)
print(f"Inserted User-Item ID: {user_item_id}")

# Query for user-items
query = {"user_id": "user123"}
user_items = query_user_items(client, "mystorytime", "user_items", query)

# Extract and print the user ID, story ID, and summary for each user-item
for user_item in user_items:
    user_id = extract_field(user_item, "user_id")
    story_id = extract_field(user_item, "story_id")
    summary = extract_field(user_item, "summary")
    print(f"User ID: {user_id}, Story ID: {story_id}, Summary: {summary}")

client.close()