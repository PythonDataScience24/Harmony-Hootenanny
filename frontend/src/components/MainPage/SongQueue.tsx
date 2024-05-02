import { Box, Paper, Stack, styled } from '@mui/material'
import React from 'react'

const SongItem = styled('div')({
  padding: '1em',
  boxSizing: 'border-box',
  backgroundColor: '#F8F9FA',
  color: '#343a40'
})

function SongQueue() {
  return (
    <Box sx={{ width: '100%', height:'100%', backgroundColor:'#f0f2f5', padding: '1em', boxSizing:'border-box'}}>
      <Stack spacing={2}>
        <SongItem>Song1</SongItem>
        <SongItem>Song2</SongItem>
        <SongItem>Song3</SongItem>
        <SongItem>Song4</SongItem>
      </Stack>
    </Box>
  )
}

export default SongQueue