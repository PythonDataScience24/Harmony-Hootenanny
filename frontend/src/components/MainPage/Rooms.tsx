import { Box, Stack } from '@mui/material'
import React from 'react'

function Rooms() {
  return (
    <Box sx={{ width: '100%', height:'100%', padding:'1em', backgroundColor: 'lightgrey' }}>
      <Stack spacing={2}>
        <div>Room1</div>
        <div>Room2</div>
        <div>Room3</div>
      </Stack>
    </Box>
  )
}

export default Rooms