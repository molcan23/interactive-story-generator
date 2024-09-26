import pymongo
import requests
import os
from dotenv import load_dotenv
import torch
from transformers import AutoTokenizer, AutoModel

from langchain.llms import OpenAI
from langchain import LLMChain, PromptTemplate

# MongoDB Atlas connection
load_dotenv()
client = pymongo.MongoClient(
    os.environ.get("ATLAS_URI"),
    connectTimeoutMS=60000
)
db = client.your_database_name  # Replace with your database name
story_collection = db.story_parts  # Replace with your story parts collection name


def generate_embedding(text: str, model_name="sentence-transformers/all-MiniLM-L6-v2") -> torch.Tensor:
    """
    Generates an embedding for the given text using the specified Hugging Face model.

    Args:
        text (str): The text to be embedded.
        model_name (str, optional): The name of the Hugging Face model to use. Defaults to "sentence-transformers/all-MiniLM-L6-v2".

    Returns:
        torch.Tensor: The generated embedding.
    """

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)

    # Extract the last hidden state for sentence-level embeddings
    embeddings = outputs.last_hidden_state.mean(dim=1)

    return embeddings


def update_embedding(story_parts: list[dict]) -> torch.Tensor:
    """
    Updates the embedding for a list of story parts.

    Args:
        story_parts (list[dict]): A list of story parts, each represented as a dictionary with "text" and "order" keys.

    Returns:
        torch.Tensor: The updated embedding.
    """

    # Combine the text from all story parts
    combined_text = " ".join([part["text"] for part in story_parts])

    # Generate the embedding for the combined text
    embedding = generate_embedding(combined_text)

    return embedding


def get_chat_history(story_id: str) -> tuple[list[str], torch.Tensor]:
    """
    Retrieves the chat history and embedding for a given story ID.

    Args:
        story_id (str): The unique identifier for the story.

    Returns:
        tuple[list[str], torch.Tensor]: A tuple containing the chat history as a list of strings and the embedding as a PyTorch tensor.
    """

    story_parts = story_collection.find({"story_id": story_id}).sort("order", 1)  # Sort by order for chronological retrieval
    chat_history = [part["text"] for part in story_parts]
    embedding = update_embedding(list(story_parts))  # Convert story_parts to list for embedding
    return chat_history, embedding


def save_story_part(story_id: str, text: str, order: int) -> None:
    """
    Saves a new story part to the database.

    Args:
        story_id (str): The unique identifier for the story.
        text (str): The text of the story part.
        order (int): The order of the story part within the story.
    """

    story_part = {"story_id": story_id, "text": text, "order": order}
    story_collection.insert_one(story_part)


# Main conversation loop
story_id = "story_000001"

while True:
    chat_history, embedding = get_chat_history(story_id)
    #
    # Your existing LLMChain code goes here, using chat_history and embedding
    # ... (replace "..." with your LLMChain logic)
    # ...

    # After processing, save the new story part
    new_story_part = "ALALALA" # ... (generate the new story part text)
    order = story_collection.find({"story_id": story_id}).count() + 1  # Get next order
    save_story_part(story_id, new_story_part, order)