import React, { useState, useEffect } from 'react'
import AudioPlayer from 'react-h5-audio-player';
import 'react-h5-audio-player/lib/styles.css';


function App() {


  const [message, setMessage] = useState();

  useEffect(() => {
    fetch('http://localhost:5000/api/greet')
      .then(response => response.json())
      .then(data => setMessage(data.message))
      .catch(error => console.error('Error:', error));
  }, []);

  const songs = ["Men At Work - Down Under (Official HD Video).mp3", "Men At Work - Down Under (Official HD Video).mp3"]
  return (
    <>
      <div>{message}</div>
      <div style={{width:"500px"}}>

      <AudioPlayer
        autoPlay
        src="Men At Work - Down Under (Official HD Video).mp3"
        showSkipControls={true}
        onPlay={e => console.log("onPlay")}
        ></AudioPlayer>
        </div>
    </>
  )
}

export default App