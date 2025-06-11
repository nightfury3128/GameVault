import React, { useState, useEffect } from 'react'; // Added useEffect
import axios from 'axios'; // Import axios
import './App.css';
import GameForm from './components/GameForm';
import GameCard from './components/GameCard';
import GameModal from './components/GameModal';
import ThemeToggle from './components/ThemeToggle';
import LoadingSpinner from './components/LoadingSpinner';

function App() {
  const [games, setGames] = useState([]);
  const [selectedGame, setSelectedGame] = useState(null);
  const [loading, setLoading] = useState(false);
  const [theme, setTheme] = useState('light'); // 'light' or 'dark'
  const [error, setError] = useState(''); // For API errors

  // Load theme from local storage and apply
  useEffect(() => {
    const storedTheme = localStorage.getItem('theme');
    const initialTheme = storedTheme ? storedTheme : 'light';
    setTheme(initialTheme);
    document.documentElement.setAttribute('data-theme', initialTheme);
  }, []);

  const handleSearchSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError(''); // Clear previous errors
    setGames([]); // Clear previous game list

    const formData = new FormData(event.target);
    const dirs = formData.get('directories');

    try {
      // Assuming Flask backend is running on port 5000
      const response = await axios.post('http://localhost:5000/api/search_games', {
        directories: dirs
      });
      setGames(response.data);
    } catch (err) {
      console.error("Error fetching game data:", err);
      setError(err.response?.data?.error || 'Failed to fetch game data. Ensure the backend server is running and accessible.');
    } finally {
      setLoading(false);
    }
  };

  const handleCardClick = (game) => {
    if (!game.error) {
      setSelectedGame(game);
    }
  };

  const handleCloseModal = () => {
    setSelectedGame(null);
  };

  const handleThemeToggle = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme); // Save theme to local storage
    document.documentElement.setAttribute('data-theme', newTheme); // Apply to HTML element for global CSS
  };

  return (
    <div className="App"> {/* Theme class is now on html via data-theme attribute */}
      <ThemeToggle onToggle={handleThemeToggle} currentTheme={theme} />
      <h1>Game Data Finder - React</h1>
      <GameForm onSubmit={handleSearchSubmit} />

      {loading && <LoadingSpinner />}
      {error && <p className="error-message">Error: {error}</p>}

      <div className='game-list'>
        {games.length === 0 && !loading && !error && <p>No games found. Try a new search.</p>}
        {games.map((game, index) => (
          // Use a more stable key if possible, e.g., game.id or unique folder path
          <div key={game.folder ? (game.folder + '-' + index) : index} onClick={() => handleCardClick(game)}>
            <GameCard game={game} />
          </div>
        ))}
      </div>

      {selectedGame && <GameModal game={selectedGame} onClose={handleCloseModal} />}
    </div>
  );
}

export default App;
