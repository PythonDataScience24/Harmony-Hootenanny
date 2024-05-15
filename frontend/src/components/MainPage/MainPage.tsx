import { Box, Divider } from '@mui/material'
import React, { useEffect, useState } from 'react'
import Rooms from './Rooms'
import MainWindow from './MainWindow'
import SongQueue from './SongQueue'
import Cookies from 'js-cookie'
import socket from '../../socket'

function MainPage() {
  const [messages, setMessages] = useState([]);
  const [data, setData] = useState();
  const [queue, setQueue] = useState();
  const [playing, setPlaying] = useState("");
  const [progress, setProgress] = useState(0);

  let userData = "";
  if (Cookies.get("userData")) {
    //@ts-ignore
    userData = JSON.parse(Cookies.get("userData"));
  }
  useEffect(() => {
    // Connect when the component mounts
    socket.connect();

    // Emit "join_room" event
    //@ts-ignore
    socket.emit("join_room", 1, userData.username);

    // Listen for "chat" events
    socket.on("song_queue", (message) => {
      setQueue(message.queue);
    });
    socket.on("currently_playing", (message) => {
      setPlaying(message.track);
      setProgress(Number(message.progress));
    });

    // Clean up: disconnect when the component unmounts
    return () => {
      socket.disconnect();
    };
  }, []); // Empty dependency array ensures this effect runs only once

  useEffect(() => { console.log(data) }, [data])

  return (
    <>
      <Box
        sx={{
          display: "flex",
          width: "100%",
          justifyContent: "space-around"
        }}
      >
        <Box sx={{ flexGrow: 1 }}>
          <Rooms></Rooms>
        </Box>

        <Divider orientation="vertical" />
        <Box sx={{ flexGrow: 7, height: "100%" }}>
          <MainWindow currentlyPlaying={playing} progress={progress}></MainWindow>
        </Box>

        <Divider orientation="vertical" />
        <Box sx={{ flexGrow: 1 }}>
          {
            // @ts-ignore
            <SongQueue queue={queue}></SongQueue>}
        </Box>
      </Box >
    </>
  )
}

export default MainPage