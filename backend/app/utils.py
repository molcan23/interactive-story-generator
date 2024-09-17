import requests
import os
from google.cloud import texttospeech
from dotenv import load_dotenv
from huggingface_hub import InferenceApi
from PIL import Image
from io import BytesIO
import base64
from langchain_ollama import OllamaLLM


# Load environment variables
load_dotenv()

model = OllamaLLM(model="llama3")


# Generate story part using Hugging Face model
def generate_story_part(
        genre="sci-fi",
        topic="colors in spanish",
        keywords=["aliens", "moon"],  # default should be a list
        choice=None,
        story_part=0,
        length_of_story=10,
        story_summary=None,
):
    # TODO: parameters from curl are not correct (order, Nones)
    print(f"SUMMARY: {story_summary}")
    print(f"GENRE: {genre}")
    print(f"TOPIC: {topic}")
    print(f"KEYWORDS: {keywords}")
    print("\n\n")

    prompt = f"Generate a story part {story_part} of {length_of_story}"
    if choice:
        prompt += (f"Continuing the story \"{story_summary}\" based on the choice: \"{choice}\". "
                  f"Directly continue with the story, so be careful about any inconsistencies! "
                  f"Be careful about repeating sentences in the whole story, sudden changes of places,"
                  f" characters and items")
    else:
        # Generate the initial part of the story
        prompt += (f"Generate an introduction 60-70 words long to a story."
                  f"Genre: {genre}, Keywords: {keywords}, Teaching topic: {topic} - do not forget to include "
                  f"at least one learning thing in the whole story!")

    prompt += f"""
        Return ONLY a json dictionary with the following keys: 
        - \"new_story_part\" with the generated story (at least 60 words) as the value,
        - \"story_summary\" with the previous story summary with additional 
            sentence (10-15 words) summarizing the currently generated story part,
        - \"choice 1\" and \"choice 2\" with 2 options for the user to choose from for continuing the story.
        
        Try to include the teaching topic provided - subtly teach the (kid) user.
        
        If the story should end (part {length_of_story} of {length_of_story}), end the story with some nice ending and
        return None for the both choices and the story_summary.   
    """

    print(prompt)
    story = model.invoke(input=prompt)
    print()
    print(story)

    return story


# Convert story text to audio using Google Cloud Text-to-Speech
def text_to_speech(text):
    client = texttospeech.TextToSpeechClient()

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
    response = client.synthesize_speech(
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
