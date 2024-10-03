from flask import Flask, request, jsonify
from flask import send_file
from gtts import gTTS
from app import app
from app.utils import generate_story_part, get_chat_history, save_story_part, parse_story_response
from app.prompt_templates import story_specification_template
import random
import requests


@app.route('/start_story', methods=['POST'])
def start_story():
    data = request.json
    narrative = data.get('narrative')
    learning_topic = data.get('learning_topic')
    number_of_parts = int(data.get('number_of_parts'))

    # Generate the first part of the story
    story_id = f"story_{str(random.randint(0, 100000))}"
    user_id = "user123"

    response = generate_story_part(story_id, user_id, narrative, learning_topic, number_of_parts)

    # Parse the generated response
    parsed_response = parse_story_response(response)

    # Save the first part of the story in MongoDB
    save_story_part(story_id, user_id, 1, parsed_response['story_text'], order=-1)

    return jsonify({
        "story_id": story_id,
        "story_name": parsed_response["story_name"],
        "story_text": parsed_response["story_text"],
        "choices": [parsed_response["choice_a"], parsed_response["choice_b"]]
    })


@app.route('/continue_story', methods=['POST'])
def continue_story():
    data = request.json
    story_id = data.get('story_id')

    if not story_id:
        return jsonify({"error": "Story ID is required"}), 400

    narrative = data.get('narrative')
    learning_topic = data.get('learning_topic')

    # TODO
    # Get current chat history and part number
    user_id = "user123"

    story_summary, part_num = get_chat_history(story_id, user_id)

    if not story_summary:
        return jsonify({"error": "No previous parts found"}), 404

    response = generate_story_part(
        story_id, user_id, narrative, learning_topic,
        number_of_parts=str(part_num + 1), part_num=part_num + 1, story_summary=story_summary
    )

    # Parse the generated response
    parsed_response = parse_story_response(response)

    # Save new part in MongoDB
    save_story_part(story_id, user_id, part_num + 1, parsed_response['story_text'], order=-1)

    return jsonify({
        "story_text": parsed_response["story_text"],
        "choices": [parsed_response["choice_a"], parsed_response["choice_b"]]
    })


@app.route('/generate_voice', methods=['POST'])
def generate_voice():
    data = request.json
    text = data.get('text', '')

    if not text:
        return jsonify({"error": "Text is required"}), 400

    # Generate audio using gTTS
    tts = gTTS(text=text, lang='en')
    audio_file_path = 'story.mp3'  # You may want to make this unique per story part
    tts.save(audio_file_path)

    return send_file(audio_file_path, as_attachment=True)


@app.route('/generate_image', methods=['POST'])
def generate_image():
    data = request.json
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    # Example using a placeholder image service (replace with actual image generation API)
    response = requests.get(f"https://api.example.com/generate-image?prompt={prompt}")

    if response.status_code != 200:
        return jsonify({"error": "Failed to generate image"}), 500

    image_url = response.json().get('image_url')  # Adjust according to the API response structure

    return jsonify({"image_url": image_url})
