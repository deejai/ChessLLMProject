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
    <div>
      <div id="Chessboard" />
      <button id="chessButtonStart" onClick={startGame}>Start</button>
      <button id="chessButtonClear" onClick={clearBoard}>Clear</button>
    </div>
  );
};

export default Chessgame;
