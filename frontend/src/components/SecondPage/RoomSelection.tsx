import React from 'react';
import {Routes, Route, Link } from "react-router-dom";
import Room from './Room';
import { Box, Button } from '@mui/material';

const RoomSelection: React.FC = () => {
  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      height="100vh"
      width="100vw"
      gap={2}
      margin="auto"
    >
      <Box
        display="flex"
        flexDirection="column"
        alignItems="center"
        justifyContent="center"
        gap={2}
        padding={2}
        border={1}
        borderRadius={2}
        borderColor="divider"
        width="60%"
      >
        <Button variant="contained" component={Link} to="/main" style={{fontSize: '20px', height: '60px', width: '100%'}}>Raum 1</Button>
        <Button variant="contained" component={Link} to="/main" style={{fontSize: '20px', height: '60px', width: '100%'}}>Raum 2</Button>
        <Button variant="contained" component={Link} to="/main" style={{fontSize: '20px', height: '60px', width: '100%'}}>Raum 3</Button>
      </Box>

      <Routes>
        <Route path="/room1" element={<Room name="Raum 1" />} />
        <Route path="/room2" element={<Room name="Raum 2" />} />
        <Route path="/room3" element={<Room name="Raum 3" />} />
      </Routes>
    </Box>
  );
}

export default RoomSelection;