import { Box } from '@mui/material'
import React, { useEffect, useState } from 'react'
import AudioPlayer from "react-h5-audio-player";
import "react-h5-audio-player/lib/styles.css";
import AutoCompleteComponent from '../AutoCompleteComponent';
import { PeopleInChannel } from './PeopleInChannel';

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
    const users = ["Aline", "Jerry", "Nils", "Janina"]
    return (
        <Box
            sx={{
                display: 'flex',
                flexDirection: "column",
                justifyContent: "space-between",
                alignItems: "strech",
                height: "100%",
                width: "100%",
            }}
        >
            <Box
                sx={{
                    display: 'flex',
                    flexDirection: "column",
                    alignItems: "center",
                }}
            >
                <PeopleInChannel users={users} />
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
                <div style={{ borderRadius:'30px', overflow: 'hidden', width: '80%', marginBottom: "100px" }}>
                    <AudioPlayer
                        autoPlay
                        src={`${backendUrl}/stream/mp3/${filename}`}
                        showSkipControls={true}
                        onPlay={(e) => console.log('onPlay')}
                        style={{ backgroundColor: '#F2F2F2' }}
                    />
                </div>
            </Box>
        </Box>
    )
}

export default MainWindow