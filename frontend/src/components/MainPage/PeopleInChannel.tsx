import { Box, Stack, useTheme, Paper } from '@mui/material';



export function PeopleInChannel({ users }: { users: string[]; }) {

    const theme = useTheme();
    return (
        <Paper
            elevation={1}
            sx={{
                margin: "10px auto 10px auto",
                padding: "15px", // Innenabstand
                width: "95%",
            }}>
            <Stack direction={"row"} gap={2}>
                {users.map((name) => {
                    return (
                        <Paper key={name} elevation={5}>
                            <Box key={name} p={1} display={"flex"} gap={1} justifyContent={"center"} >
                                <svg height="24" width="24">
                                    <circle r="10" cx="12" cy="12" fill="lightgray" />
                                </svg>
                                <div>
                                    {name}
                                </div>
                            </Box>
                        </Paper>)
                })}

            </Stack>
        </Paper>
    );
}
