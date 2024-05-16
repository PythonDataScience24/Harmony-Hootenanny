import { Box, Divider } from '@mui/material'
import React, { act, useEffect, useState } from 'react'
import Rooms from './Rooms'
import MainWindow from './MainWindow'
import SongQueue from './SongQueue'
import Cookies from 'js-cookie'
import socket from '../../socket'

interface MainPageProps {
  roomId: number;
}
const MainPage: React.FC<MainPageProps> = ({ roomId }) =>{
  const [messages, setMessages] = useState([]);
  const [data, setData] = useState();
  const [queue, setQueue] = useState();
  const [playing, setPlaying] = useState("");
  const [progress, setProgress] = useState(0);
  const [activeUsers, setactiveUsers] = useState();

  let userData = "";
  if (Cookies.get("userData")) {
    //@ts-ignore
    userData = JSON.parse(Cookies.get("userData"));
  }
  useEffect(()=>{
    console.log(activeUsers)
  },[activeUsers])
  useEffect(() => {
    // Connect when the component mounts
    socket.connect();

    // Emit "join_room" event
    //@ts-ignore
    socket.emit("join_room", roomId, userData.username);

    // Listen for "chat" events
    socket.on("song_queue", (message) => {
      setQueue(message.queue);
    });
    socket.on("active_users", (message) => {
      setactiveUsers(message.users);
    });
    socket.on("currently_playing", (message) => {
      // {'title': 'Summer Vibes', 'artist': 'Sunny Beats', 
      // 'filename': 'https://example.com/song1.mp3', 
      // 'progress': -7079, 'queue_index': 1}
      setPlaying(message.filename);
      setProgress(Number(message.progress));
    });

    // Clean up: disconnect when the component unmounts
    return () => {
      socket.disconnect();
    };
  }, [roomId]); // This effect runs whenever roomId changes

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
          <MainWindow currentlyPlaying={playing} progress={progress} activeUsers={activeUsers}></MainWindow>
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

export function MainPage1(){
  return <MainPage roomId={1} />;
}
export function MainPage2(){
  return <MainPage roomId={2}/>;
}
export function MainPage3(){
  return <MainPage roomId={3}/>;
}