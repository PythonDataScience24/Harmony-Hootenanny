import { Box, Stack } from '@mui/material'
import React from 'react'

function Rooms() {
  return (
    <Box sx={{height:'100%', padding:'1em', boxSizing:'border-box', backgroundColor: '#DEE2E6' }}>
      <Stack spacing={2}>
        <div>Room1</div>
        <div>Room2</div>
        <div>Room3</div>
      </Stack>
    </Box>
  )
}

export default Rooms