# Interactive Story Generator: Frontend and Backend Integration

## TODO

/project-root
  /frontend
    Dockerfile
    # other frontend files
  /backend
    Dockerfile
    # other backend files
  docker-compose.yml
  # other root files

## Overview

The **Interactive Story Generator** consists of a **React** frontend and a **Flask** backend. The frontend handles user interaction and displays content, while the backend processes story generation, text-to-speech, and image creation.

## How They Work Together

1. **Frontend Interaction**:
   - The user interacts with the **React frontend** by submitting a form with parameters like genre, length, and keywords for the story.
   - The **React frontend** sends a POST request to the Flask backend API (`/generate-story`) with this data.
   - The **Flask backend** processes the request, generates the story using the Hugging Face model, converts the text to speech using Google Text-to-Speech (TTS), and returns the story and audio to the frontend.
   - The frontend receives the response and displays the generated story, while the **audio** is played using an HTML `<audio>` element.
   - The user is presented with options (choices) for how the story should continue. The frontend then sends another POST request to the backend (`/generate-next-story-part`) with the selected choice.
   - The backend generates the next part of the story and returns it along with new audio. The frontend updates the story and continues the process.

2. **Backend Interaction**:
   - The **Flask backend** receives requests for generating the story and story continuation, processes them using AI models (Hugging Face for story generation, Google TTS for audio generation), and returns the story text and the encoded audio back to the frontend.
   - For each part of the story, the backend is also responsible for generating and returning a new image using a text-to-image model.
   - This interaction is done via JSON payloads between the frontend and backend.

## Data Flow

1. **User Input**:
   - **Frontend (React)** → **Backend (Flask)**
   - **Endpoint**: `/generate-story` (POST)
   - **Payload**:
     ```json
     {
       "genre": "Fantasy",
       "length": 10,
       "keywords": "dragon, knight"
     }
     ```
   - **Backend Response**:
     ```json
     {
       "story": "Once upon a time...",
       "audio": "base64-encoded-audio-string"
     }
     ```

2. **Story Display and Choices**:
   - **Frontend (React)** → **Backend (Flask)**
   - **Endpoint**: `/generate-next-story-part` (POST)
   - **Payload**:
     ```json
     {
       "choice": "The knight decides to face the dragon."
     }
     ```
   - **Backend Response**:
     ```json
     {
       "story": "The knight bravely charges towards the dragon...",
       "audio": "base64-encoded-audio-string",
       "choices": [
         "The knight draws his sword.",
         "The knight tries to talk to the dragon.",
         "The knight runs away."
       ]
     }
     ```

3. **Image Generation**:
   - **Frontend (React)** → **Backend (Flask)**
   - **Endpoint**: `/generate-image` (POST)
   - **Payload**:
     ```json
     {
       "story_text": "The knight charges towards the dragon."
     }
     ```
   - **Backend Response**:
     ```json
     {
       "image": "base64-encoded-image-string"
     }
     ```

## CORS (Cross-Origin Resource Sharing)

Since the frontend and backend are on different ports (React on `3000`, Flask on `5000`), **CORS** needs to be handled. The Flask backend uses **`Flask-CORS`** to allow cross-origin requests from the React frontend.

In `app/__init__.py`, `CORS(app)` is used to allow these requests.

## Configuration

1. **Frontend API Endpoint**:
   - Set the API URL in the frontend's `.env` file:
     ```
     REACT_APP_BACKEND_URL=http://localhost:5000
     ```

2. **Backend API**:
   - The backend runs on `http://localhost:5000` and exposes routes for story generation, continuation, and image generation.

## Dockerization for Deployment

To deploy both frontend and backend in a containerized environment, use **Docker**.

### Docker Setup for Backend

Create a `Dockerfile` for the backend:

```Dockerfile
# Use Python official image
FROM python:3.9-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the Flask port
EXPOSE 5000

# Start the application
CMD ["python", "run.py"]
