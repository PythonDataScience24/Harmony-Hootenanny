import { Box, Paper, Stack, styled } from '@mui/material'
import React from 'react'

function SongQueue() {
  return (
    <Box sx={{ width: '100%' }}>
      <Stack spacing={2}>
        <div>Song1</div>
        <div>Song2</div>
        <div>Song3</div>
        <div>Song4</div>
      </Stack>
    </Box>
  )
}

export default SongQueue