import React, { useState } from 'react';
import StoryForm from './components/StoryForm';
import StoryDisplay from './components/StoryDisplay';
import './App.css';

function App() {
  const [story, setStory] = useState(null);
  const [audio, setAudio] = useState(null);

  const handleStoryGenerated = (generatedStory, generatedAudio) => {
    setStory(generatedStory);
    setAudio(generatedAudio);
  };

  return (
    <div className="App">
      <h1>Interactive Story Generator</h1>
      {!story ? (
        <StoryForm onStoryGenerated={handleStoryGenerated} />
      ) : (
        <StoryDisplay story={story} audio={audio} setStory={setStory} />
      )}
    </div>
  );
}

export default App;
