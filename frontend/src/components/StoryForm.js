import React, { useState } from 'react';
import axios from 'axios';

function StoryForm({ onStoryGenerated }) {
  const [genre, setGenre] = useState('');
  const [length, setLength] = useState('');
  const [keywords, setKeywords] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const params = { genre, length, keywords };
    try {
      const response = await axios.post('http://localhost:5000/generate-story', params);
      onStoryGenerated(response.data.story, response.data.audio);
    } catch (error) {
      console.error('Error generating story:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Genre:</label>
        <input
          type="text"
          value={genre}
          onChange={(e) => setGenre(e.target.value)}
          required
        />
      </div>
      <div>
        <label>Length (minutes):</label>
        <input
          type="number"
          value={length}
          onChange={(e) => setLength(e.target.value)}
          required
        />
      </div>
      <div>
        <label>Keywords:</label>
        <input
          type="text"
          value={keywords}
          onChange={(e) => setKeywords(e.target.value)}
        />
      </div>
      <button type="submit">Generate Story</button>
    </form>
  );
}

export default StoryForm;
