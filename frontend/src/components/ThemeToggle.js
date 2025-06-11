import React from 'react';

function ThemeToggle({ onToggle, currentTheme }) {
  return (
    <button onClick={onToggle} style={{ position: 'absolute', top: '20px', right: '20px', padding: '10px 15px', zIndex: '100' }}>
      Toggle to {currentTheme === 'light' ? 'Dark' : 'Light'} Mode
    </button>
  );
}

export default ThemeToggle;
