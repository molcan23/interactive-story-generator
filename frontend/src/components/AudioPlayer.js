import React from 'react';

function AudioPlayer({ audio }) {
  return (
    <div>
      <h3>Listen to the Story:</h3>
      {audio && <audio controls src={`data:audio/wav;base64,${audio}`} />}
    </div>
  );
}

export default AudioPlayer;
