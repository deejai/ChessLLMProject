import React, { useState } from 'react';
import { TextField, Button, CircularProgress, Box } from '@mui/material';

const ChatInterface = () => {
  const [response, setResponse] = useState('');
  const [elo, setElo] = useState(1000); // Default ELO
  const [isLoading, setIsLoading] = useState(false);

  const dummyFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"; // Dummy FEN

  const handleAskClick = async () => {
    setIsLoading(true);

    try {
      const payload = {
        fen: dummyFEN,
        elo: elo,
      };

      const response = await fetch('https://hogbod.dev/chess-llm-coach-api/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      const jsonResponse = await response.json();
      const responseText = jsonResponse.data.response;
      setResponse(responseText);
    } catch (error) {
      console.error('Error:', error);
      setResponse('An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box display="flex" flexDirection="column" alignItems="center">
      <TextField
        id="elo-input"
        label="Your ELO"
        type="number"
        variant="outlined"
        value={elo}
        onChange={(e) => setElo(Math.max(0, parseInt(e.target.value)))}
        inputProps={{ min: "0" }}
        style={{ width: '80px', marginTop: '16px', marginBottom: '16px' }}
      />
      <Box display="flex" flexDirection="column" alignItems="center">
        <Button
          id="prompt-button"
          variant="contained"
          color="primary"
          onClick={handleAskClick}
          disabled={isLoading}
          style={{ marginBottom: '16px' }}
        >
          Coach's Advice
        </Button>
        {isLoading ? <CircularProgress /> : <span id="prompt-response">{response}</span>}
      </Box>
    </Box>
  );
};

export default ChatInterface;
