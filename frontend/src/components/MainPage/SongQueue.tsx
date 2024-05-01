import { Box, Paper, Stack, styled } from '@mui/material'
import React from 'react'

const SongItem = styled('div')({
  padding: '1em'
})

function SongQueue() {
  return (
    <Box sx={{ width: '100%',padding:'1em' }}>
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