import { Box, Divider } from "@mui/material";
import MainPage from "./components/MainPage/MainPage";
import SecondPage from "./components/SecondPage";
import RoomSelection from "./components/SecondPage/RoomSelection";
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import { StrictMode, useMemo } from "react";
import useMediaQuery from '@mui/material/useMediaQuery';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { DARK_THEME } from "./colorthemes";

export default function App() {
  const router = createBrowserRouter([
    {
      path: "/",
      element: <RoomSelection />,
    },
    {
      path: "/main",
      element: <MainPage />,
    }, {
      path: "/test",
      element: <SecondPage />
    }
  ])
  const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)');
  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode: prefersDarkMode ? 'dark' : 'light',
        },
      }),
    [prefersDarkMode],
  );
  return (
    <StrictMode>
      <ThemeProvider theme={theme}>
        <CssBaseline enableColorScheme />
        <Box height={"10vh"} marginLeft="20px"alignContent={"center"}>
        <h1>Harmony Hootenany</h1>
        </Box>        
        <Divider/>
        <Box height={"87vh"} sx={{ display: "flex", width: '100vw' }}>
          <RouterProvider router={router} />
        </Box>
      </ThemeProvider>
    </StrictMode>
  );
}

