# Interactive Story Generator for Kids

This project is an **interactive story generator** that creates custom stories for kids. The app allows users to input story parameters (genre, length, keywords, etc.), which generates a personalized story using AI models. The story progresses interactively with user choices, and each decision leads to the generation of new story parts. Additionally, the app includes **audio narration** and **visual illustrations** based on the generated content. 

The application is built with **React** on the frontend and **Flask** on the backend. It integrates **text-to-text** models, **text-to-speech** services, and **text-to-image** models to provide a rich, interactive experience.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Frontend](#frontend)
- [Backend](#backend)
- [Story and Image Generation](#story-and-image-generation)
- [Future Enhancements](#future-enhancements)

## Features

- Generate custom, interactive stories based on user input.
- Present children with multiple-choice decision points to progress the story.
- Provide **audio narration** using text-to-speech (TTS) services.
- Generate illustrations for each part of the story using **text-to-image models**.
- Ensure consistency in art style and character design throughout the story.
- Deployable via **Docker** and scalable using **Kubernetes**.

## Technologies Used

### Frontend (React)
- **React** for building interactive user interfaces.
- Dynamic rendering for displaying story text, decision options, and images.
- **Audio playback** of generated story narration.

### Backend (Flask)
- **Flask** for serving API requests and handling story generation, TTS, and image generation.
- **Hugging Face Text Generation Models** to generate dynamic story content based on user input and decisions.
- **Text-to-Speech Services** (Google TTS, Amazon Polly) to convert story text into speech.
- **Text-to-Image Models** (e.g., Stable Diffusion, DALL-E) to generate illustrations for the story.

### Deployment
- **Docker** for containerizing the web application, ensuring a consistent development and production environment.
- **Kubernetes** (future enhancement) for scaling the application to handle multiple users simultaneously.

## Setup and Installation

### Prerequisites
- **Node.js** and **npm** for frontend development.
- **Python 3.x+** and **Flask** for the backend.  -- TBD
- **Docker** for containerization.

### Installation Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-repo/interactive-story-generator.git
   cd interactive-story-generator
   

2. **LLama 3 8B model usage**
   
- First, login needs to be done via
   ```bash
   pip install -U "huggingface_hub[cli]"
   huggingface-cli login

- Then, models need to be downloaded  
   ```bash
   huggingface-cli download meta-llama/Meta-Llama-3-8B-Instruct --exclude "original/*" --local-dir meta-llama/Meta-Llama-3-8B-Instruct```