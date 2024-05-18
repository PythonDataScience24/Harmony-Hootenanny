import { Box, Paper, Stack, styled } from '@mui/material'
import React from 'react'

function SongQueue({ queue }: { queue: [JSON] }) {
  //@ts-ignore
  let songList;
  if (queue === undefined) {
    songList = [
      {
        title: "Not loaded yet",
        artist: "",
        duration: ""
      }
    ]
  } else {
    songList = queue;
  }

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
                    {//@ts-ignore
                      <Box >Title: {song.title}</Box>
                    }
                    {//@ts-ignore
                      <Box>Artist: {song.artist}</Box>
                    }
                    {//@ts-ignore
                      <Box>Duration: {Math.floor(song.duration / 60)}:{song.duration - Math.floor(song.duration / 60) * 60}</Box>
                    }
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