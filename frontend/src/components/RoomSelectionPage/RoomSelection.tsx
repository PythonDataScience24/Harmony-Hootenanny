import React, { useState, useEffect } from "react";
import { Routes, Route, Link, useNavigate } from "react-router-dom";
import { Box, Button, Typography } from "@mui/material";
import { MainPage1, MainPage2, MainPage3 } from "../MainPage/MainPage";
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
      navigate(roomPath);
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
          onClick={() => handleRoomClick("/main/room1")}
          style={{ fontSize: "20px", height: "60px", width: "100%" }}
        >
          Room 1
        </Button>
        <Button
          variant="contained"
          onClick={() => handleRoomClick("/main/room2")}
          style={{ fontSize: "20px", height: "60px", width: "100%" }}
        >
          Room 2
        </Button>
        <Button
          variant="contained"
          onClick={() => handleRoomClick("/main/room3")}
          style={{ fontSize: "20px", height: "60px", width: "100%" }}
        >
          Room 3
        </Button>
      </Box>

      {/* <Routes>
        <Route path="/main/room1" element={<MainPage1 />} />
        <Route path="/main/room2" element={<MainPage2 />} />
        <Route path="/main/room3" element={<MainPage3 />} />
      </Routes> */}
    </Box>
  );
};

export default RoomSelection;
