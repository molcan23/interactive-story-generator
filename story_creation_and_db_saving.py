import pymongo
import requests
import os
from dotenv import load_dotenv
import torch
from transformers import AutoTokenizer, AutoModel

# from langchain_community.llms import HuggingFaceInference
from langchain import LLMChain, PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_huggingface import HuggingFacePipeline
from huggingface_hub import login

login()
load_dotenv()


# MongoDB Atlas connection
client = pymongo.MongoClient(
    os.environ.get("ATLAS_URI"),
    connectTimeoutMS=60000
)

db = client.your_database_name  # Replace with your database name
story_collection = db.story_parts  # Replace with your story parts collection name


def get_chat_history(story_id: str, user_id: str) -> tuple[list[str], str]:
    """
    Retrieves the chat history and concatenated summary for a given story ID and user ID.

    Args:
        story_id (str): The unique identifier for the story.
        user_id (str): The unique identifier for the user.

    Returns:
        tuple[list[str], str]: A tuple containing the chat history as a list of strings and the concatenated summary as a string.
    """

    story_parts = story_collection.find({"story_id": story_id, "user_id": user_id}).sort("order", 1)  # Sort by order for chronological retrieval
    chat_history = [part["text"] for part in story_parts]
    concatenated_summary = " ".join([part["text"] for part in story_parts])  # Concatenate summaries
    return chat_history, concatenated_summary


def save_story_part(story_id: str, user_id: str, text: str, order: int) -> None:
    """
    Saves a new story part to the database.

    Args:
        story_id (str): The unique identifier for the story.
        user_id (str): The unique identifier for the user.
        text (str): The text of the story part.
        order (int): The order of the story part within the story.
    """

    story_part = {"story_id": story_id, "user_id": user_id, "text": text, "order": order}
    story_collection.insert_one(story_part)


# Initialize memory
cass_buff_memory = ConversationBufferMemory()

# Prompt template
template = """
You are now the guide of a mystical journey in the Whispering Woods.
A traveler named Elara seeks the lost Gem of Serenity.
You must navigate her through challenges, choices, and consequences,
dynamically adapting the tale based on the traveler's decisions.
Your goal is to create a branching narrative experience where each choice
leads to a new path, ultimately determining Elara's fate.

Here are some rules to follow:
1. Start by asking the player to choose some kind of weapons that will be used later in the game
2. Have a few paths that lead to success
3. Have some paths that lead to death. If the user dies generate a response that explains the death and ends in the text: "The End.", I will search for this text to end the game

Here is the chat history, use this to understand what to say next: {chat_history}
Human: {human_input}
AI:"""

prompt = PromptTemplate(
    input_variables=["chat_history", "human_input"],
    template=template
)

# Replace 'path/to/your/llama-3-model' with the actual path to your LLaMA 3 model
llm = HuggingFacePipeline.from_model_id(
    model_id="meta-llama/Llama-3.1-8B",
    task="text-generation",
)


llm_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=cass_buff_memory
)

# Main conversation loop
story_id = "story_000001"
user_id = "user123"

while True:
    chat_history, concatenated_summary = get_chat_history(story_id, user_id)

    # Generate a response using the LLMChain
    response = llm_chain.run(chat_history=chat_history, human_input=input("What are you doing"))

    # Check if the response indicates the end of the game
    if "The End." in response:
        break

    # Save the new story part
    save_story_part(story_id, user_id, response, order=-1)