import React, { useState, useEffect } from 'react';
import { Chess } from 'chess.js';
import { useChess } from './ChessContext';

const Chessgame = () => {
  const [board, setBoard] = useState(null);
  const [game, setGame] = useState(new Chess());
  const [turn, setTurn] = useState('White');
  const { fen, setFen } = useChess();

  useEffect(() => {
    const newBoard = Chessboard('Chessboard', {
      position: 'start',
      draggable: true,
      pieceTheme: 'img/chesspieces/{piece}.png',
      onDragStart: (source, piece, position, orientation) => {
        if (game.isCheckmate() || game.isDraw()) {
          return false;
        }
        if ((game.turn() === 'w' && piece.search(/^b/) !== -1) ||
            (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
          return false;
        }
      },
      onDrop: (source, target) => {
        try {
          game.move({
            from: source,
            to: target,
            promotion: 'q'
          });

          setTurn(game.turn() === 'w' ? 'White' : 'Black');
          setFen(game.fen());
        } catch (e) {
          console.log("Invalid move");
        }
      },
      onMouseoutSquare: () => {},
      onMouseoverSquare: () => {},
      onSnapEnd: () => {
        setBoard(prevBoard => {
          prevBoard.position(game.fen());
          return prevBoard;
        });
      },
    });
    setBoard(newBoard);
  }, [game]);

  const resetGame = () => {
    if (board) {
      board.clear();
      setGame(new Chess());
    }
    setTurn('White');
  };

  const getFEN = () => {
    if (game) {
      alert(game.fen());
    }
  };

  return (
    <div style={{ textAlign: 'center' }}>
      <div>
        {turn} to Move
      </div>
      <div
        id="Chessboard"
        style={{
          width: '600px',
          height: '600px',
          margin: '0 auto',
          border: '1px solid black',
        }}
      />
      <button id="chessButtonClear" onClick={resetGame} style={{ margin: '10px' }}>
        Reset
      </button>
      <button id="chessButtonFEN" onClick={getFEN}>
        Get FEN
      </button>
    </div>
  );
};

export default Chessgame;
