import React, { createContext, useContext, useState } from 'react';

const ChessContext = createContext();

export const useChess = () => {
  return useContext(ChessContext);
};

export const ChessProvider = ({ children }) => {
  const [fen, setFen] = useState('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1');
  
  return (
    <ChessContext.Provider value={{ fen, setFen }}>
      {children}
    </ChessContext.Provider>
  );
};
