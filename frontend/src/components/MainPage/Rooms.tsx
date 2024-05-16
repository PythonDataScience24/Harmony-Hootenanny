import { Box, Button, Stack } from '@mui/material'
import React from 'react'
import { useTheme } from '@mui/material/styles';
import { Link, useLocation} from 'react-router-dom';

function Rooms() {
  
  const theme = useTheme();
  //console.log(JSON.stringify(theme.palette));
  const location = useLocation();
  const roomStyle = (roomPath: string)=> ({

    width: "100%",
    backgroundColor: location.pathname === roomPath ? theme.palette.primary.main : theme.palette.background.paper,
    color: location.pathname === roomPath ? theme.palette.primary.contrastText : theme.palette.text.primary,

  });
  return (
    <Box sx={{height:'100%', padding:'1em', boxSizing:'border-box', backgroundColor: theme.palette.background.paper , width:"100%"}}>
      <Stack spacing={2}>
      <Box sx={{border: '1px solid', borderColor: theme.palette.divider, borderRadius: 1, boxShadow: 1}}>
          <Button component={Link} to="/main/room1" style={roomStyle("/main/room1")}>Room1</Button>
        </Box>
        <Box sx={{border: '1px solid', borderColor: theme.palette.divider, borderRadius: 1, boxShadow: 1}}>
          <Button component={Link} to="/main/room2" style={roomStyle("/main/room2")}>Room2</Button>
        </Box>
        <Box sx={{border: '1px solid', borderColor: theme.palette.divider, borderRadius: 1, boxShadow: 1}}>
          <Button component={Link} to="/main/room3" style={roomStyle("/main/room3")}>Room3</Button>
        </Box>
      </Stack>
    </Box>
  )
}

export default Rooms