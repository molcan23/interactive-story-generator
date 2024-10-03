# Interactive Story Generator

## Overview

The Interactive Story Generator is a web application that allows users to create and continue stories interactively. The backend is built using Flask, which handles story generation, voice synthesis, and image generation. The frontend is a simple HTML/CSS/JavaScript interface that communicates with the backend via RESTful API calls.

## Project Structure

project_root/
├── backend/
│ ├── app.py
│ ├── routes.py
│ ├── utils.py
│ ├── prompt_templates.py
│ ├── run.py
│ └── backhand_variables.py
└── frontend/
├── index.html
├── script.js
└── styles.css


## Backend Flow

1. **Flask Application**:
    - The Flask application runs on `http://127.0.0.1:5000`.
    - It has the following main endpoints:
        - **`/start_story`**: Starts a new story based on user input.
        - **`/continue_story`**: Continues an existing story using a provided story ID.
        - **`/generate_voice`**: Generates audio from text using Google Text-to-Speech.
        - **`/generate_image`**: Generates an image based on a text prompt.

2. **Database Connection**:
    - The backend connects to a MongoDB database to store and retrieve story parts.

3. **Generating Voice and Images**:
    - The backend uses the `gTTS` library for generating voice audio from text.
    - It can call an external API to generate images based on prompts.

## Frontend Flow

1. **HTML Interface**:
    - The frontend consists of an HTML file (`index.html`) with input fields for narrative, learning topic, and number of parts.
    - It displays the generated story parts, a button to play audio, and an area to show generated images.

2. **JavaScript Interactions**:
    - The frontend uses JavaScript (`script.js`) to handle user interactions.
    - It sends POST requests to the Flask API endpoints to start or continue stories.
    - It fetches generated voice audio and images after each part is created.

3. **User Actions**:
    - Users can start a new story by entering details in the input fields and clicking "Start Story."
    - Users can continue an existing story by entering the corresponding story ID when prompted.

## How to Use

### Step 1: Run the Backend

1. Navigate to the `backend` directory in your terminal.
2. Run the Flask application:

   ```bash
   python run.py


### Step 2: Serve the Frontend

1. Navigate to the frontend directory in your terminal.
2. Start a simple HTTP server:
- For Python 3:
    ```bash
    python -m http.server 8000

### Step 3: Access the Application
1. Open your web browser.
2. Go to http://127.0.0.1:8000.
3. Use the interface to start or continue stories.

### Example Usage
- To start a new story, enter values in the input fields and click "Start Story."
- To continue a story, enter the generated story ID when prompted by clicking "Continue Story."

### Features
- Story Generation: Create engaging stories based on user-defined narratives and learning topics.
- Voice Playback: Listen to each part of the story read aloud using generated voice audio.
- Image Generation: View images related to each part of the story, generated based on prompts.
