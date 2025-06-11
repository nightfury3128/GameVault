import React from 'react';

function GameForm({ onSubmit }) {
  // Basic form structure
  return (
    <form onSubmit={onSubmit}>
      <input type='text' name='directories' placeholder='Enter directory paths' />
      <button type='submit'>Search</button>
    </form>
  );
}

export default GameForm;
