import { Box, Divider } from '@mui/material'
import React, { useEffect, useState } from 'react'
import Rooms from './Rooms'
import MainWindow from './MainWindow'
import SongQueue from './SongQueue'
import Cookies from 'js-cookie'
import socket from '../../socket'
import DashBoard from '../DashBoard'

interface MainPageProps {
  roomId: number;
}
const MainPage: React.FC<MainPageProps> = ({ roomId }) => {
  const [queue, setQueue] = useState();
  const [progress, setProgress] = useState(0);
  const [activeUsers, setactiveUsers] = useState();
  const [filename, setFilename] = useState("");
  const [song, setSong] = useState({});

  let userData = "";
  if (Cookies.get("userData")) {
    //@ts-ignore
    userData = JSON.parse(Cookies.get("userData"));
  }
  useEffect(() => {
    //console.log(activeUsers)
  }, [activeUsers])
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
      // 'progress': -7079}

      setSong({
        title:message.title,
        artist:message.artist
      })
      setFilename(encodeURIComponent(message.filename));
      encodeURIComponent(message.filename)
      setProgress(Number(message.progress));
      const audioElement = document.querySelector('audio');
      if (audioElement) {
        // Update the current time
        console.log(progress)
        audioElement.currentTime = message.progress;
        //playAudio(audioElement);
      } else {
        console.error('No <audio> element found on the page.');
      }
    })
    socket.on("pause_song", (message) => {
      const audioElement = document.querySelector('audio');
      if (audioElement) {
        // Update the current time
        audioElement.pause();
        //playAudio(audioElement);
      } else {
        console.error('No <audio> element found on the page.');
      }
      console.log(message)
    });
    socket.on("play_song", (message) => {
      console.log(message)
      const audioElement = document.querySelector('audio');
      if (audioElement) {
        // Update the current time an play
        audioElement.play();
        audioElement.currentTime = message.progress;
      } else {
        console.error('No <audio> element found on the page.');
      }
    });
    // Clean up: disconnect when the component unmounts
    return () => {
      socket.disconnect();
    };
  }, [roomId]); // This effect runs whenever roomId changes

  const skip = () => {
    socket.connect();
    //@ts-ignore
    socket.emit("skip_song", roomId, userData.username);
  };
  const play = () => {
    socket.connect();
    socket.emit("play_song", roomId);
  };
  const pause = () => {
    socket.connect();
    socket.emit("pause_song", roomId);
  };
  const select_song = (new_song: string) =>{
    socket.connect();
    socket.emit("select_song", new_song, roomId);
  }
  const download_song = (url: string) =>{
    socket.connect();
    socket.emit("download_song", url, roomId);
  }
  return (
    <>
      <Box
        sx={{
          display: "flex",
          width: "100%",
          justifyContent: "space-around"
        }}
      >
        <Box>
          <Rooms></Rooms>
        </Box>
        <Divider orientation="vertical" />
        <Box sx={{ flexGrow: 7, height: "100%" }}>
          {//@ts-ignore
            roomId > 0 ? <MainWindow 
            currentlyPlaying={filename} 
            activeUsers={activeUsers} 
            skip={skip} 
            play={play} 
            pause={pause} 
            onSongSelect={select_song}
            onSongDownload={download_song}
            //@ts-ignore
            song={song} 
            >  
            </MainWindow> :
              <DashBoard />
          }
        </Box>

        {roomId > 0 ? <>
          <Divider orientation="vertical" />
          <Box sx={{ flexGrow: 1 }}>
            {
              // @ts-ignore
              <SongQueue queue={queue}></SongQueue>}
          </Box>
        </> : <></>
        }
      </Box >
    </>
  )
}

export function MainPage1() {
  return <MainPage roomId={1} />;
}
export function MainPage2() {
  return <MainPage roomId={2} />;
}
export function MainPage3() {
  return <MainPage roomId={3} />;
}
export function Dashboard() {
  return <MainPage roomId={0} />;
}