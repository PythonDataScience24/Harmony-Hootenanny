import { Box } from '@mui/material'
import { useState } from 'react'
import AudioPlayer from "react-h5-audio-player";
import "react-h5-audio-player/lib/styles.css";
import AutoCompleteComponent from '../AutoCompleteComponent';
import { PeopleInChannel } from './PeopleInChannel';

function MainWindow({ currentlyPlaying, activeUsers, skip, play, pause, song, onSongSelect, onSongDownload}:
    {
        currentlyPlaying: string,
        activeUsers?: string[],
        skip: () => void,
        play: () => void,
        pause: () => void,
        song: JSON,
        onSongSelect: (new_song: string) => void,
        onSongDownload: (new_song: string) => void,
    }) {
    const [filename, setFilename] = useState(encodeURIComponent(currentlyPlaying));
    const backendUrl = "http://localhost:5000";
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
                        onSongSelect={onSongSelect}
                        onSongDownload={onSongDownload}
                    />
                </div>
            </Box>
            <Box
                sx={{
                    display: 'flex',
                    justifyContent: "center",
                }}
            >
                <h3>                        
                {//@ts-ignore
                        song.title
                    } - 
                {//@ts-ignore
                    song.artist
                }
                </h3>
            </Box>
            <Box
                sx={{
                    display: 'flex',
                    justifyContent: "center",
                }}
            >
                <div style={{ borderRadius: '30px', overflow: 'hidden', width: '80%', marginBottom: "100px" }}>

                    <AudioPlayer
                        loop
                        muted
                        src={`${backendUrl}/stream/mp3/${currentlyPlaying}`}
                        showSkipControls={true}
                        onPlay={play}
                        onPause={pause}
                        onClickNext={skip}
                        style={{ backgroundColor: '#F2F2F2' }}
                    />
                </div>
            </Box>
        </Box>
    )
}

export default MainWindow