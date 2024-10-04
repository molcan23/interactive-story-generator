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
            // Displaying Story Name
            document.getElementById('story-name').innerText = data.story_name;

            // Displaying Story Text
            document.getElementById('story-summary').value = data.story_text;

            // Displaying Choices
            const choiceAButton = document.getElementById('choice-a');
            const choiceBButton = document.getElementById('choice-b');

            choiceAButton.innerText = data.choices[0]; // Set text for Choice A
            choiceBButton.innerText = data.choices[1]; // Set text for Choice B

            choiceAButton.style.display = 'inline'; // Show Choice A button
            choiceBButton.style.display = 'inline'; // Show Choice B button

            document.getElementById('response').innerText = "Story started successfully!";

            // Add event listeners for choices
            choiceAButton.onclick = () => handleChoice(data.story_id, 'A'); // Pass story ID and choice type
            choiceBButton.onclick = () => handleChoice(data.story_id, 'B'); // Pass story ID and choice type

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
                // Displaying Story Text
                document.getElementById('story-summary').value += "\n\n" + data.story_text; // Append new part to the summary

                // Displaying Choices
                const choiceAButton = document.getElementById('choice-a');
                const choiceBButton = document.getElementById('choice-b');

                choiceAButton.innerText = data.choices[0]; // Set text for Choice A
                choiceBButton.innerText = data.choices[1]; // Set text for Choice B

                choiceAButton.style.display = 'inline'; // Show Choice A button
                choiceBButton.style.display = 'inline'; // Show Choice B button

                document.getElementById('response').innerText = "Story continued successfully!";

                // Add event listeners for choices (optional)
                choiceAButton.onclick = () => handleChoice(data.story_id, 'A'); // Pass story ID and choice type
                choiceBButton.onclick = () => handleChoice(data.story_id, 'B'); // Pass story ID and choice type
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('response').innerText = "Error continuing story.";
        });
}

// Function to handle user choices (optional)
function handleChoice(storyId, choiceType) {
    fetch(`http://127.0.0.1:5000/make_choice`, {  // Update this URL as needed based on your backend setup
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            story_id: storyId,
            choice: choiceType  // Send which choice was made (A or B)
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(`Error making a choice: ${data.error}`);
            } else {
                alert(`You selected Choice ${choiceType}: ${data.message}`);  // Assuming response includes a message about the outcome of the choice.

                // Optionally update UI or continue with new story parts based on the response.
                document.getElementById('story-summary').value += "\n\n" + data.new_story_part;  // Example of updating UI with new content.

                // Update choices again if necessary:
                const newChoices = data.new_choices;  // Assuming your API returns new choices after making a selection.
                if (newChoices) {
                    const choiceAButton = document.getElementById('choice-a');
                    const choiceBButton = document.getElementById('choice-b');

                    choiceAButton.innerText = newChoices[0];
                    choiceBButton.innerText = newChoices[1];

                    choiceAButton.style.display = 'inline';
                    choiceBButton.style.display = 'inline';
                }

            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}