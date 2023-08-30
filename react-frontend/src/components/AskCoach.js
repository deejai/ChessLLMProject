import React, { useState, useEffect } from 'react';
import { TextField, Button, CircularProgress, Box } from '@mui/material';
import { useChess } from './ChessContext';

const ChatInterface = () => {
  const [response, setResponse] = useState('');
  const [elo, setElo] = useState(1000);
  const [isLoading, setIsLoading] = useState(false);
  const [taskId, setTaskId] = useState(null);
  const { fen } = useChess();

  const checkTaskStatus = async () => {
    try {
      const response = await fetch(`https://hogbod.dev/chess-llm-coach-api/get-gpt-response/${taskId}`);
      const jsonResponse = await response.json();
      
      if (response.status === 200 && jsonResponse.status === 'done') {
        setResponse(jsonResponse.result);
        setIsLoading(false);
        setTaskId(null);
      } else if (response.status === 404) {
        setResponse('Task not found.');
        setIsLoading(false);
        setTaskId(null);
      }
    } catch (error) {
      console.error('Error:', error);
      setResponse('An error occurred while checking task status.');
      setIsLoading(false);
      setTaskId(null);
    }
  };
  
  const handleAskClick = async () => {
    setIsLoading(true);
  
    try {
      const payload = {
        fen: fen,
        elo: elo,
      };
  
      const response = await fetch('https://hogbod.dev/chess-llm-coach-api/ask-coach', {
        method: 'POST',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
  
      if (response.status === 202) {
        const jsonResponse = await response.json();
        setTaskId(jsonResponse.data.task_id);
      } else {
        setResponse('Failed to create task.');
        setIsLoading(false);
      }
      
    } catch (error) {
      console.error('Error:', error);
      setResponse('An error occurred.');
      setIsLoading(false);
    }
  };
  
  useEffect(() => {
    let intervalId;
    
    if (taskId) {
      intervalId = setInterval(() => {
        checkTaskStatus();
      }, 1000);
    }
    
    return () => clearInterval(intervalId);
  }, [taskId]);

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
