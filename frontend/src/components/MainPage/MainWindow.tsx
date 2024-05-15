import { Box } from '@mui/material'
import React, { useEffect, useState } from 'react'
import AudioPlayer from "react-h5-audio-player";
import "react-h5-audio-player/lib/styles.css";
import AutoCompleteComponent from '../AutoCompleteComponent';
import { PeopleInChannel } from './PeopleInChannel';
import socket from '../../socket';
import Cookies from 'js-cookie';

function MainWindow({ currentlyPlaying, progress, activeUsers }: { currentlyPlaying: string, progress: number, activeUsers?: string[]}) {
    const [filename, setFilename] = useState(encodeURIComponent(currentlyPlaying));
    const backendUrl = "http://localhost:5000";
    const users = ["Aline", "Jerry", "Nils", "Janina"]


    // Find the existing <audio> element on the page
    const audioElement = document.querySelector('audio');
    if (audioElement) {
        // Update the current time
        audioElement.currentTime = progress;
    } else {
        console.error('No <audio> element found on the page.');
    }
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
                <PeopleInChannel users={activeUsers} />
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
                <div style={{ borderRadius: '30px', overflow: 'hidden', width: '80%', marginBottom: "100px" }}>
                    <AudioPlayer
                        src={`${backendUrl}/stream/mp3/${encodeURIComponent(currentlyPlaying)}`}
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