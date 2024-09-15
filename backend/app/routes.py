from flask import Blueprint, request, jsonify
# from .utils import generate_story_part, text_to_speech, generate_image
from utils_mock import generate_story_part, text_to_speech, generate_image

story_bp = Blueprint('story', __name__)

# Route for generating the initial story
@story_bp.route('/generate-story', methods=['POST'])
def generate_story():
    data = request.json
    genre = data.get('genre')
    length = data.get('length')
    keywords = data.get('keywords')

    story = generate_story_part(genre, length, keywords)
    audio = text_to_speech(story)

    return jsonify({'story': story, 'audio': audio})

# Route for generating the next part of the story based on user choice
@story_bp.route('/generate-next-story-part', methods=['POST'])
def continue_story():
    data = request.json
    choice = data.get('choice')

    # Generate the next part of the story based on the user's choice
    story = generate_story_part(None, None, None, choice=choice)
    audio = text_to_speech(story)

    # Provide new choices for the user
    choices = ["Continue with option 1", "Continue with option 2", "Continue with option 3"]

    return jsonify({'story': story, 'audio': audio, 'choices': choices})

# Route for generating an image based on the story content
@story_bp.route('/generate-image', methods=['POST'])
def generate_image_endpoint():
    data = request.json
    story_text = data.get('story_text')

    image = generate_image(story_text)
    return jsonify({'image': image})