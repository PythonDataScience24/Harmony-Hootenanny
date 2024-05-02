import { Box, Stack } from '@mui/material'
import React from 'react'
import { useTheme } from '@mui/material/styles';

function Rooms() {
  
  const theme = useTheme();
  //console.log(JSON.stringify(theme.palette));
  return (
    <Box sx={{height:'100%', padding:'1em', boxSizing:'border-box', backgroundColor: theme.palette.background.paper , width:"100%"}}>
      <Stack spacing={2}>
        <div style={{width:"100%"}}>Room1</div>
        <div>Room2</div>
        <div>Room3</div>
      </Stack>
    </Box>
  )
}

export default Rooms