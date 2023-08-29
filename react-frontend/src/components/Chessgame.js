import React, { useState, useEffect } from 'react';
import { Chess } from 'chess.js';

const Chessgame = () => {
  const [game, setGame] = useState(null);

  useEffect(() => {
    const newGame = Chessboard(
      'Chessboard',
      {
        position: 'start',
        pieceTheme: 'img/chesspieces/{piece}.png'
      }
    );
    setGame(newGame);
  }, []);

  const startGame = () => {
    if (game) {
      game.start();
    }
  }

  const clearBoard = () => {
    if (game) {
      game.clear();
    }
  }

  return (
    <div style={{ textAlign: 'center' }}>
      <div 
        id="Chessboard"
        style={{
          width: '800px',
          height: '800px',
          margin: '0 auto',
          border: '1px solid black'
        }}
      />
      <button id="chessButtonStart" onClick={startGame}>Start</button>
      <button id="chessButtonClear" onClick={clearBoard}>Clear</button>
    </div>
  );
};

export default Chessgame;
