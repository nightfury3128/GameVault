import React from 'react';

function GameCard({ game }) {
  // Basic card structure
  return (
    <div className='game-card'>
      {game.error ? (
        <>
          <p><strong>Folder:</strong> {game.folder}</p>
          <p><strong>Error:</strong> {game.error}</p>
        </>
      ) : (
        <>
          <img src={game.background_image} alt={game.name} style={{ width: '100px' }} />
          <h5>{game.name}</h5>
          <p>Release Date: {game.release_date}</p>
          <p>Metacritic: {game.metacritic}</p>
        </>
      )}
    </div>
  );
}

export default GameCard;
