import requests
import os
from google.cloud import texttospeech
from PIL import Image
from io import BytesIO
import base64
import pymongo
from dotenv import load_dotenv
from .prompt_templates import story_specification_template

from .backand_variables import llama_model


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
        story_id: str, user_id: str,
        narrative,  learning_topic, number_of_parts, part_num=1,
        story_summary="Beginning", user_input="Random choice"):

    print(f"STORY_ID: {story_id}")
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


# Convert story text to audio using Google Cloud Text-to-Speech
def text_to_speech(text):
    speech_client = texttospeech.TextToSpeechClient()

    # Setup input text
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Define the voice parameters
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",  # You can choose other voices
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Define audio configuration
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    # Synthesize speech
    response = speech_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Convert audio to base64 encoding
    audio_content = base64.b64encode(response.audio_content).decode('utf-8')
    return audio_content


# # Generate image based on the story using a text-to-image model
# def generate_image(story_text):
#     # Placeholder image generation using PIL
#     # In production, use a text-to-image model like DALL-E or Stable Diffusion
#     img = Image.new('RGB', (200, 200), color=(73, 109, 137))
#
#     # Create image bytes
#     img_byte_arr = BytesIO()
#     img.save(img_byte_arr, format='PNG')
#     img_byte_arr = img_byte_arr.getvalue()
#
#     # Encode image to base64
#     encoded_img = base64.b64encode(img_byte_arr).decode('utf-8')
#
#     return encoded_img

def parse_story_response(response):
    print(f"RESPONSE: {response}\n\n")
    response = str(response).strip()

    if 'WHAT WILL YOU DO?' in response:
        parts = response.split('WHAT WILL YOU DO?')
    else:
        exit()  # raise ValueError('Expected section header for choices not found in the last section.')

    body = parts[0]

    # Extract choices part
    choices = parts[1].strip().lower().split("\n")

    # print(f"BODY: {body}\n\n")
    # print(f"BODY: {body}\n\n")
    print(f"PARTS: {parts}\n\n")
    # print(parts, "\n\n")
    print(f"CHOICES: {choices[0]}\n\n")
    print(choices)
    # print(f"CHOICES: {parts}\n\n")

    # Split on 'A) ' and 'B) ' to get choices
    choice_a = choices[0]
    choice_b = choices[1]

    # Return a dictionary with the parsed elements
    return {
        "story_name": "STORY NAME TODO",
        "story_text": body,
        "choice_a": choice_a,
        "choice_b": choice_b
    }
