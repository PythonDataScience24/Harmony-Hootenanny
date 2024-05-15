import React, { useState, useEffect } from "react";
import { Routes, Route, Link, useNavigate } from "react-router-dom";
import Room from "./Room";
import { Box, Button, Typography } from "@mui/material";
import { MusicNote } from "@mui/icons-material";
import { useAuth } from "../contexts/AuthContext";
import Cookies from "js-cookie";

const RoomSelection: React.FC = () => {
  const { isLoggedIn } = useAuth();
  const [username, setUsername] = useState<string>("");
  const navigate = useNavigate();

  useEffect(() => {
    // Retrieve the username from the cookies
    const userDataJson = Cookies.get("userData");
    if (userDataJson) {
      const userData = JSON.parse(userDataJson);
      // Extract the username and save it in a variable
      const username: string = userData.username;
      setUsername(username);
      console.log(username); // Output: qwert
    } else {
      console.log("No user data found in cookies.");
    }
  }, []);

  const handleRoomClick = (roomPath: string) => {
    if (isLoggedIn) {
      navigate("/main");
    } else {
      navigate("/login");
    }
  };
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
      {isLoggedIn ? (
        <Typography variant="h4" gutterBottom>
          Welcome {username}{" "}
          <MusicNote style={{ fontSize: 40, verticalAlign: "middle" }} />
        </Typography>
      ) : (
        <Typography variant="h4" gutterBottom>
          Welcome to the Music Room Selection{" "}
          <MusicNote style={{ fontSize: 40, verticalAlign: "middle" }} />
        </Typography>
      )}
      <Typography variant="body1" gutterBottom>
        You need to be logged in to join a room. Please log in or sign up if you
        haven't already.
      </Typography>
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
        <Button
          variant="contained"
          style={{ fontSize: "20px", height: "60px", width: "100%" }}
          onClick={() => handleRoomClick("/room1")}
        >
          Raum 1
        </Button>
        <Button
          variant="contained"
          style={{ fontSize: "20px", height: "60px", width: "100%" }}
          onClick={() => handleRoomClick("/room2")}
        >
          Raum 2
        </Button>
        <Button
          variant="contained"
          style={{ fontSize: "20px", height: "60px", width: "100%" }}
          onClick={() => handleRoomClick("/room3")}
        >
          Raum 3
        </Button>
      </Box>

      <Routes>
        <Route path="/room1" element={<Room name="Raum 1" />} />
        <Route path="/room2" element={<Room name="Raum 2" />} />
        <Route path="/room3" element={<Room name="Raum 3" />} />
      </Routes>
    </Box>
  );
};

export default RoomSelection;
