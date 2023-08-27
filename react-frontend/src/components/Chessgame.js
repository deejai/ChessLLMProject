import React, { useState, useEffect } from 'react';
import { Chessboard } from 'react-chessboard';
import { Chess } from 'chess.js';

const Chessgame = () => {
  const [game, setGame] = useState(new Chess());

  const handleMove = (move) => {
    console.log('Attempting to make move:', move);

    const newGame = new Chess(game.fen());
    const result = newGame.move(move);

    if (result !== null) {
      setGame(newGame);
    } else {
      console.log('Invalid move');
    }
  };
  
  const fen = game.fen();

  return (
    <div>
      <Chessboard id="Chessboard" 
                  width={400} 
                  position={fen} 
                  onPieceDrop={({sourceSquare, targetSquare}) => {
                    handleMove({from: sourceSquare, to: targetSquare});
                  }} 
      />
    </div>
  );
};

export default Chessgame;
