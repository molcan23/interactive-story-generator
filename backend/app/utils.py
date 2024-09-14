import requests
import os
from google.cloud import texttospeech
from dotenv import load_dotenv
from huggingface_hub import InferenceApi
from PIL import Image
from io import BytesIO
import base64

load_dotenv()

# Hugging Face API for text generation
huggingface_api = InferenceApi(repo_id="gpt-2", token=os.getenv('HUGGINGFACE_API_KEY'))

# Generate story part using Hugging Face model
def generate_story_part(genre, length, keywords, choice=None):
    prompt = ""
    if choice:
        prompt = choice  # Use the user's choice to continue the story
    else:
        # Generate the initial part of the story
        prompt = f"Genre: {genre}, Length: {length}, Keywords: {keywords}"

    response = huggingface_api(prompt)
    story = response[0]['generated_text']

    return story

# Convert story text to audio using Google Cloud Text-to-Speech
def text_to_speech(text):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", 
        name="en-US-Wavenet-D",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    audio_content = base64.b64encode(response.audio_content).decode('utf-8')
    return audio_content

# Generate image using text-to-image models
def generate_image(story_text):
    # Here, we'll use a sample image generation API.
    # In a real-world scenario, you would use a model like DALL-E or Stable Diffusion
    # to generate an image from text.
    img = Image.new('RGB', (200, 200), color=(73, 109, 137))

    # Create image bytes
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    # Encode image to base64
    encoded_img = base64.b64encode(img_byte_arr).decode('utf-8')

    return encoded_img
