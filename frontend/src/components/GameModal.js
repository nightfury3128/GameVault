import React from 'react';

function GameModal({ game, onClose }) {
  if (!game) return null;

  // Basic modal structure
  return (
    <div className='modal'>
      <div className='modal-content'>
        <span className='close-button' onClick={onClose}>&times;</span>
        <h2>{game.name}</h2>
        <img src={game.background_image} alt={game.name} style={{ width: '150px' }} />
        <p><strong>Release Date:</strong> {game.release_date}</p>
        <p><strong>Metacritic Score:</strong> {game.metacritic}</p>
        <p><strong>Description:</strong> {game.description}</p>
        <p><strong>Genres:</strong> {game.genres}</p>
      </div>
    </div>
  );
}

export default GameModal;
