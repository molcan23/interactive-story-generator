import os
import random
import pymongo
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
# from langchain_ollama import OllamaLLM

# Remote Llama
from langchain_ollama.llms import OllamaLLM
llama_model = OllamaLLM(model="llama3.1")

# # Local Llama - not really
# from langchain_community.llms import Ollama
# llama_model = Ollama(model="mistral")

# login()
load_dotenv()

# MongoDB Atlas connection
client = pymongo.MongoClient(
    os.environ.get("ATLAS_URI"),
    connectTimeoutMS=60000
)

db = client.mystorytime  # Replace with your database name
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

    story_parts = (
        story_collection.find({"story_id": story_id, "user_id": user_id}).sort("order", 1)
    )

    if not story_parts:
        return "", 1

    story_parts_list = []
    part_num = -1

    for part in story_parts:
        story_parts_list.append(part["text"])
        part_num = part["part_num"]
        
    # Concatenate summaries
    concatenated_summary = " ".join(story_parts_list)

    # return chat_history, concatenated_summary
    return concatenated_summary, part_num


def save_story_part(story_id: str, user_id: str, part_num: int, text: str, order: int) -> None:
    """
    Saves a new story part to the database.

    Args:
        story_id (str): The unique identifier for the story.
        user_id (str): The unique identifier for the user.
        text (str): The text of the story part.
        order (int): The order of the story part within the story.
    """

    story_part = {"story_id": story_id, "user_id": user_id, "part_num": part_num, "text": text, "order": order}
    story_collection.insert_one(story_part)


def generate_story_part(
        narrative,  learning_topic, number_of_parts, part_num=1,
        story_summary="Beginning", user_input="Random choice"):
    # Create a runnable sequence with prompt and LLM using pipe operator
    runnable_sequence = story_specification_template | llama_model

    # Prepare inputs as a dictionary for invocation
    inputs = {
        "narrative": narrative,
        "learning_topic": learning_topic,
        "number_of_parts": number_of_parts,
        "part_num": part_num,
        "story_summary": story_summary,
        "user_input": user_input
    }

    # Generate a response using the runnable sequence
    response = runnable_sequence.invoke(inputs)

    # Save the new story part
    save_story_part(story_id, user_id, part_num, response, order=-1)

    return response


# TODO uncomment when chain is working
# narrative = input("Choose the narrative:\n")
# learning_topic = input("Choose the learning topic:\n")
# number_of_parts = input("Choose the story length:\n")
# story_summary = ""

narrative = "shrek"
learning_topic = "spanish colors"
number_of_parts = "3"
story_summary = ""

# This feature needs to be tested (#words/minute etc.)
# length = input("Choose the length of the story:\n")


# Define the prompt template using ChatPromptTemplate
story_specification_template = ChatPromptTemplate.from_template(
    f"""
    You are now the narrator of an exciting story for kids.
    The story plot revolves around {{narrative}}.

    Use the following context to seamlessly continue the story: 
    Here is the current story summary: {{story_summary}} 

    Your task is to create an engaging tale that begins with a unique and captivating opening each time.
    Ensure that each part is distinct and does not repeat or reference earlier parts explicitly, but maintains continuity.

    As you narrate, guide the user (kid) through thrilling challenges, choices, and consequences,
    dynamically adapting the tale based on their decisions. Each choice should lead to a new and unexpected path.

    Here are some guidelines to follow:
    1. Begin each story part with a distinct and creative opening that captures attention.
    2. Each story part should contain 150-200 words and end after {{number_of_parts}} parts.
    3. Introduce new challenges or twists in every part to keep the narrative exciting and engaging.
    4. Integrate the learning topic naturally into the story without disrupting its flow.
    5. Each story part must end strictly with two choices marked as A and B, without any additional text, 
    except for the last one (number {{number_of_parts}}).

    This is the story part number {{part_num}}.
    
    Emphasizing, if {{part_num}} is equal to {{number_of_parts}} story MUST finish with an ending 
    (with conclusion) and with The end.
    

    AI:
    """
)

# TODO: fix the ending of the story so it actually ends after 'number_of_pats'

# Main conversation loop
story_id = f"story_{str(random.randint(0, 100000))}"
user_id = "user123"

response = generate_story_part(narrative,  learning_topic, number_of_parts)

print(response)

while True:
    story_summary, part_num = get_chat_history(story_id, user_id)

    user_input = input("What do you want to do?\n")

    response = generate_story_part(narrative,  learning_topic, number_of_parts, part_num+1, story_summary, user_input)

    print(response)

    # Check if the response indicates the end of the game
    if "The End." in response:
        break

    print(f"\nHISTORY: {story_summary[:20]}\nPART NUM: {part_num}\n")


client.close()
