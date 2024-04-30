import React, { useState, useEffect } from "react";
import AudioPlayer from "react-h5-audio-player";
import "react-h5-audio-player/lib/styles.css";
import AutoCompleteComponent from "./AutoCompleteComponent";

export default function App() {
  const [message, setMessage] = useState();
  const [filename, setFilename] = useState(""); // Empty string throws 404 error on first load
  const backendUrl = "http://localhost:5000";

  useEffect(() => {
    fetch('http://localhost:5000/api/greet')
      .then(response => response.json())
      .then(data => setMessage(data.message))
      .catch(error => console.error('Error:', error));
  }, []);

  return (
    <>
      <div>{message}</div>
      <AutoCompleteComponent
        onSongSelect={(selectedTitle: string) =>
          setFilename(encodeURIComponent(selectedTitle))
        }
      />
      <div style={{ width: "500px" }}>
        <AudioPlayer
          autoPlay
          src={`${backendUrl}/stream/mp3/${filename}`}
          showSkipControls={true}
          onPlay={(e) => console.log("onPlay")}
        ></AudioPlayer>
      </div>
    </>
  );
}

