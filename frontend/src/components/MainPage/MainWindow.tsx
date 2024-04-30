import { Box } from '@mui/material'
import React, { useEffect, useState } from 'react'
import AudioPlayer from "react-h5-audio-player";
import "react-h5-audio-player/lib/styles.css";
import AutoCompleteComponent from '../AutoCompleteComponent';

function MainWindow() {
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
        <Box
            sx={{
                display: 'flex',
                flexDirection: "column",
                justifyContent: "space-between",
                height: "100%"
            }}
        >
            <div>People in Channel Component</div>
            <div>
                <AutoCompleteComponent
                    onSongSelect={(selectedTitle: string) =>
                        setFilename(encodeURIComponent(selectedTitle))
                    }
                />
            </div>
            <div style={{ width: "500px" }}>
                <AudioPlayer
                    autoPlay
                    src={`${backendUrl}/stream/mp3/${filename}`}
                    showSkipControls={true}
                    onPlay={(e) => console.log("onPlay")}
                ></AudioPlayer>
            </div>
        </Box>
    )
}

export default MainWindow