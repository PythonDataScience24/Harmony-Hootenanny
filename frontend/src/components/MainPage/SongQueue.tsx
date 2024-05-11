import { Box, Paper, Stack, styled } from '@mui/material'
import React from 'react'

function SongQueue() {
  const songList = [
    {
      "title": "Shape of You",
      "artist": "Ed Sheeran",
      "duration": "3:53"
    },
    {
      "title": "Bohemian Rhapsody",
      "artist": "Queen",
      "duration": "5:55"
    },
    {
      "title": "Blinding Lights",
      "artist": "The Weeknd",
      "duration": "3:20"
    },
    {
      "title": "Rolling in the Deep",
      "artist": "Adele",
      "duration": "3:48"
    },
    {
      "title": "Hotel California",
      "artist": "Eagles",
      "duration": "6:30"
    }
  ]

  return (
    <>
      <h2 style={{ margin: "20px" }}>Song Queue:</h2>
      <Box sx={{
        width: '100%', height: '85%', overflow: "auto",
        //backgroundColor:'#f0f2f5', 
        padding: '1em', boxSizing: 'border-box'
      }}>
        <Stack spacing={2}>
          {songList.map((song, index) => {
            return (
              <Box key={index}>
                {index == 0 ? <Box key={"firstSong"}>Next Up:</Box> : <></>}
                <Paper elevation={1} key={index}>
                  <Box sx={{ padding: "10px" }} display={"flex"} flexDirection={"column"} gap={"5px"} >
                    <Box >Title: {song.title}</Box>
                    <Box>Artist: {song.artist}</Box>
                    <Box>Duration: {song.duration}</Box>
                  </Box>
                </Paper>
              </Box>
            )
          })}
          {songList.map((song, index) => {
            return (
              <Box key={index}>
                <Paper elevation={1} key={index}>
                  <Box sx={{ padding: "10px" }} display={"flex"} flexDirection={"column"} gap={"5px"} >
                    <Box >Title: {song.title}</Box>
                    <Box>Artist: {song.artist}</Box>
                    <Box>Duration: {song.duration}</Box>
                  </Box>
                </Paper>
              </Box>
            )
          })}
          {songList.map((song, index) => {
            return (
              <Box key={index}>
                <Paper elevation={1} key={index}>
                  <Box sx={{ padding: "10px" }} display={"flex"} flexDirection={"column"} gap={"5px"} >
                    <Box >Title: {song.title}</Box>
                    <Box>Artist: {song.artist}</Box>
                    <Box>Duration: {song.duration}</Box>
                  </Box>
                </Paper>
              </Box>
            )
          })}
        </Stack>
      </Box>
    </>
  )
}

export default SongQueue