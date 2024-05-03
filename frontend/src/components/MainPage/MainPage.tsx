import { Box, Divider } from '@mui/material'
import React from 'react'
import Rooms from './Rooms'
import MainWindow from './MainWindow'
import SongQueue from './SongQueue'

function MainPage() {
  return (
    <>
      <Box
        sx={{
          display: "flex",
          width: "100%",
          justifyContent: "space-around"
        }}
      >
        <Box sx={{ flexGrow: 1 }}>
          <Rooms></Rooms>
        </Box>

        <Divider orientation="vertical"/>
        <Box sx={{ flexGrow: 7, height: "100%" }}>
          <MainWindow></MainWindow>
        </Box>

        <Divider orientation="vertical" />
        <Box sx={{ flexGrow: 1 }}>
          <SongQueue></SongQueue>
        </Box>
      </Box >
    </>
  )
}

export default MainPage