import React, { useState } from 'react';
import AudioPlayer from './AudioPlayer';
import axios from 'axios';

function StoryDisplay({ story, audio, setStory }) {
  const [currentStory, setCurrentStory] = useState(story);
  const [choices, setChoices] = useState(null);
  const [currentAudio, setCurrentAudio] = useState(audio);

  const handleChoice = async (choice) => {
    try {
      const response = await axios.post('http://localhost:5000/generate-next-story-part', { choice });
      setCurrentStory(response.data.story);
      setCurrentAudio(response.data.audio);
      setChoices(response.data.choices);
    } catch (error) {
      console.error('Error continuing the story:', error);
    }
  };

  return (
    <div>
      <h2>Story:</h2>
      <p>{currentStory}</p>
      <AudioPlayer audio={currentAudio} />
      {choices && (
        <div>
          <h3>Make a choice:</h3>
          {choices.map((choice, index) => (
            <button key={index} onClick={() => handleChoice(choice)}>
              {choice}
            </button>
          ))}
        </div>
      )}
      <button onClick={() => setStory(null)}>Start a New Story</button>
    </div>
  );
}

export default StoryDisplay;
