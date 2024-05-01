import { Box } from '@mui/material'
import React from 'react'

function PeopleInChannel() {
    return (
        <Box
            sx={{
                backgroundColor: "Ivory",
                marginLeft: "auto", // Abstand zum nächsten Element. em = Schriftgröße des aktuellen Elementes
                marginRight: "auto", // Abstand zum nächsten Element. em = Schriftgröße des aktuellen Elementes
                padding: "1em", // Innenabstand

            }}>
            People in Channel Component
        </Box>
    )
}

export default PeopleInChannel