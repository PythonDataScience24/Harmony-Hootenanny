import { Box } from '@mui/material'
import React, { useEffect, useState } from 'react'
import AudioPlayer from "react-h5-audio-player";
import "react-h5-audio-player/lib/styles.css";
import AutoCompleteComponent from '../AutoCompleteComponent';
import PeopleInChannel from './PeopleInChannel';

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
                alignItems: "strech", 
                height: "100%",
                width: "100%",
                backgroundColor: "#F8F9FA",

            }}
        >
            <Box
                sx={{
                    display: 'flex',
                    flexDirection: "column",
                    alignItems: "center",

                }}
            >

                <PeopleInChannel />
                <div>
                    <AutoCompleteComponent
                        onSongSelect={(selectedTitle: string) =>
                            setFilename(encodeURIComponent(selectedTitle))
                        }
                    />
                </div>
            </Box>
            <Box
                sx={{
                    display: 'flex',
                    justifyContent: "center",
                }}
            >
                <div style={{ maxWidth: "500px", width:"100%" }}>
                    <AudioPlayer
                        autoPlay
                        src={`${backendUrl}/stream/mp3/${filename}`}
                        showSkipControls={true}
                        onPlay={(e) => console.log("onPlay")}
                    ></AudioPlayer>
                </div>
            </Box>
        </Box>
    )
}

export default MainWindow