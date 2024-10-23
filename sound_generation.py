import os
import openai

api_key = os.environ.get("OPENAI_API_KEY")

your_text = 'Pink fluffy unicorn dancing on a rainbow'
client = openai.OpenAI(api_key=api_key)
response = client.audio.speech.create(
    model="tts-1",
    voice="alloy", # other voices: 'echo', 'fable', 'onyx', 'nova', 'shimmer'
    input=your_text
)
response.stream_to_file('speech.mp3')

# TODO needs to be tested
