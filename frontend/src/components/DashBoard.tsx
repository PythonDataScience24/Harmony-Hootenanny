import { Box, Button, Divider, Paper } from "@mui/material";
import React, { useEffect, useState } from "react";
import Rooms from "./MainPage/Rooms";

interface ArtistData {
  artist: string;
  count: number;
}

interface RoomData {
  top_artist: ArtistData[];
}

const DashBoard = () => {
  const [data, setData] = useState<Record<string, RoomData> | null>(null);

  useEffect(() => {
    fetch("http://localhost:5000/api/dashboard")
      .then((response) => response.json())
      .then((data) => setData(data));
  }, []);

  if (!data) {
    return <div>Loading...</div>;
  }
 
  const rowStyling = {
    width: "100%",
    padding: "20px",
    marginBottom: "50px",
    display: "flex",
    alignItems: "center",
    flexDirection: "row",
    flexWrap: "wrap",
    justifyContent: "space-around",
  }
  const paperStyling = {
    padding: "20px",
    width: "30%"
  }
  const topArtistPaperStyling = {
    padding: "20px",
    width: "25%"
  }
  const paperElevation = 1;
  return (
    <>
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          marginLeft: "auto",
          marginRight: "auto",
          marginTop: "20px",
          height: "80vh",
          overflow: "auto"
        }}
      >
        <h2 style={{ fontWeight: 'bold', fontSize: '1.5em' }}>General Data</h2>
        <Box sx={rowStyling}>
        <Box sx={rowStyling}>
        {Object.entries(data).map(([room, roomData]) => (
          <Paper key={room} sx={topArtistPaperStyling}>
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', height: '100%' }}>
              <h3 style={{ alignSelf: 'center' }}>{room}</h3>
              <Box sx={{ display: 'flex', flexDirection: 'row', alignItems: 'flex-start', width: '100%' }}>
              <h4 style={{ position: 'relative', top: '-10px' }}>Top Artists:</h4>
              <ol style={{ alignSelf: 'center', textAlign: 'left' }}>
              {roomData.top_artist.map((artistData, index) => (
                <li key={index}>{artistData.artist}</li>
          ))}
        </ol>
      </Box>
    </Box>
  </Paper>
))}
      </Box>
          <Paper elevation={paperElevation} sx={paperStyling}>
            Top Queuers: <br />
            <img src="/topQueuers.png" alt="" width={"100%"} />
          </Paper>
          <Paper elevation={paperElevation} sx={paperStyling}>
            Top Skippers: <br />
            <img src="/topSkippers.png" alt="" width={"100%"} />
          </Paper>
        </Box>



        <h2 style={{ fontWeight: 'bold', fontSize: '1.5em' }}>Most Played Songs</h2>
        <Box sx={rowStyling}>
          <Paper elevation={paperElevation} sx={paperStyling}>
            Room 1: <br />
            <img src="/topSongs1.png" alt="" width={"100%"} />
          </Paper>
          <Paper elevation={paperElevation} sx={paperStyling}>
            Room 2: <br />
            <img src="/topSongs2.png" alt="" width={"100%"} />
          </Paper>
          <Paper elevation={paperElevation} sx={paperStyling}>
            Room 3: <br />
            <img src="/topSongs3.png" alt="" width={"100%"} />
          </Paper>
        </Box>
        <h2 style={{ fontWeight: 'bold', fontSize: '1.5em' }}>Room Stats</h2>
        <Box sx={rowStyling}>
          <Paper elevation={paperElevation} sx={paperStyling}>
            Number of listeners: <br />
            <img src="/numberOfListeners.png" alt="" width={"100%"} />
          </Paper>
          <Paper elevation={paperElevation} sx={paperStyling}>
            Total Playtime: <br />
            <img src="/playtime.png" alt="" width={"100%"} />
          </Paper>
        </Box>
      </Box>
  
    </>
  );
};

export default DashBoard;