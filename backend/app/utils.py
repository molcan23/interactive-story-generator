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
def generate_story_part(genre, length, keywords, choice=None):
    prompt = ""
    if choice:
        prompt = f"Continuing the story based on the choice: {choice}"  # Continue based on the user's choice
    else:
        # Generate the initial part of the story
        prompt = f"Genre: {genre}, Length: {length} minutes, Keywords: {keywords}"

    story = model.invoke(input=prompt)

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
