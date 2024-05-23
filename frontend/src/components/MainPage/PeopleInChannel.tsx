import { Box, Stack, useTheme, Paper } from "@mui/material";

export function PeopleInChannel({ users }: { users?: string[] }) {
  function getRandomColor() {
    const colors = [
      "#FF0000", // Red
      "#FF7F00", // Orange
      "#FFFF00", // Yellow
      "#00FF00", // Green
      "#0000FF", // Blue
      "#4B0082", // Indigo
      "#9400D3", // Violet
    ];

    const randomIndex = Math.floor(Math.random() * colors.length);
    return colors[randomIndex];
  }
  return (
    <Paper
      elevation={1}
      sx={{
        margin: "10px auto 10px auto",
        padding: "15px", // Innenabstand
        width: "95%",
      }}
    >
      <Stack direction={"row"} gap={2}>
        {users &&
          users.map((name) => {
            return (
              <Paper key={name} elevation={5}>
                <Box
                  key={name}
                  p={1}
                  display={"flex"}
                  gap={1}
                  justifyContent={"center"}
                >
                  <svg height="24" width="24">
                    <circle r="10" cx="12" cy="12" fill={getRandomColor()} />
                  </svg>
                  <div>{name}</div>
                </Box>
              </Paper>
            );
          })}
      </Stack>
    </Paper>
  );
}
