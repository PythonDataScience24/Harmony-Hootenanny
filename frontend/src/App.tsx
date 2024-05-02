import { Box } from "@mui/material";
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
        <h1>Harmony Hootenany</h1>
        <Box sx={{ display: "flex", height: "80vh", width: '100vw' }}>
          <RouterProvider router={router} />
        </Box>
      </ThemeProvider>
    </StrictMode>
  );
}

