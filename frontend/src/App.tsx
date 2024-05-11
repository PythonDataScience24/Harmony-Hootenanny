import { Box, Divider } from "@mui/material";
import MainPage from "./components/MainPage/MainPage";
import SecondPage from "./components/SecondPage";
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
        <Box height={"10vh"} marginLeft="20px" alignContent={"center"}>
          <h1>Harmony Hootenany</h1>
        </Box>
        <Divider />
        <Box height={"87vh"} sx={{ display: "flex", width: '100vw' }}>
          <script src="https://cdn.socket.io/4.6.0/socket.io.min.js" integrity="sha384-c79GN5VsunZvi+Q/WObgk2in0CbZsHnjEqvFxC5DxHn9lTfNce2WW6h2pH6u/kF+" crossOrigin="anonymous"></script>
          {/*script tag is for websockets to work*/}
          <RouterProvider router={router} />
        </Box>
      </ThemeProvider>
    </StrictMode>
  );
}

