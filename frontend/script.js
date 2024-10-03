document.getElementById('start-story').addEventListener('click', startStory);
document.getElementById('continue-story').addEventListener('click', continueStory);

function startStory() {
    const narrative = document.getElementById('narrative').value;
    const learningTopic = document.getElementById('learning-topic').value;
    const numberOfParts = document.getElementById('number-of-parts').value;

    fetch('http://127.0.0.1:5000/start_story', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            narrative: narrative,
            learning_topic: learningTopic,
            number_of_parts: numberOfParts
        })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('story-summary').value = data.part; // Display the first part of the story

            // Generate voice for the story part
            fetch('http://127.0.0.1:5000/generate_voice', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: data.part })
            })
                .then(voiceResponse => voiceResponse.blob())
                .then(blob => {
                    const url = URL.createObjectURL(blob);
                    const playButton = document.getElementById('play-voice');
                    playButton.style.display = 'inline';
                    playButton.onclick = () => {
                        const audio = new Audio(url);
                        audio.play();
                    };
                });

            // Generate image for the story part
            fetch('http://127.0.0.1:5000/generate_image', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ prompt: narrative }) // Adjust prompt as needed
            })
                .then(imageResponse => imageResponse.json())
                .then(imageData => {
                    const imgElement = document.getElementById('story-image');
                    imgElement.src = imageData.image_url; // Set the generated image URL
                    imgElement.style.display = 'block'; // Show the image
                });

            document.getElementById('response').innerText = "Story started successfully!";
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('response').innerText = "Error starting story.";
        });
}

function continueStory() {
    const storyId = prompt("Enter the story ID to continue:");

    fetch('http://127.0.0.1:5000/continue_story', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            story_id: storyId
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('response').innerText = data.error; // Display error message if any
            } else {
                document.getElementById('story-summary').value += "\n\n" + data.part; // Append new part to the summary

                // Generate voice for the new story part
                fetch('http://127.0.0.1:5000/generate_voice', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ text: data.part })
                })
                    .then(voiceResponse => voiceResponse.blob())
                    .then(blob => {
                        const url = URL.createObjectURL(blob);
                        const playButton = document.getElementById('play-voice');
                        playButton.style.display = 'inline';
                        playButton.onclick = () => {
                            const audio = new Audio(url);
                            audio.play();
                        };
                    });

                // Generate image for the new story part
                fetch('http://127.0.0.1:5000/generate_image', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ prompt: data.part }) // Use appropriate prompt for image generation
                })
                    .then(imageResponse => imageResponse.json())
                    .then(imageData => {
                        const imgElement = document.getElementById('story-image');
                        imgElement.src = imageData.image_url; // Set the generated image URL
                        imgElement.style.display = 'block'; // Show the image
                    });

                document.getElementById('response').innerText = "Story continued successfully!";
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('response').innerText = "Error continuing story.";
        });
}