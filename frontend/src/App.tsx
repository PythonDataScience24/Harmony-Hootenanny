import { Box, Button, Divider, Link } from "@mui/material";
import MainPage from "./components/MainPage/MainPage";
import SecondPage from "./components/SecondPage";
import RoomSelection from "./components/SecondPage/RoomSelection";
import { Route, Routes } from "react-router-dom";
import { StrictMode, useMemo } from "react";
import useMediaQuery from "@mui/material/useMediaQuery";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import { DARK_THEME } from "./colorthemes";
import LoginLogoutButton from "./components/MainPage/LoginLogoutButton";
import AuthForm from "./components/AuthForm/AuthForm";

export default function App() {
  const prefersDarkMode = useMediaQuery("(prefers-color-scheme: dark)");
  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode: prefersDarkMode ? "dark" : "light",
        },
      }),
    [prefersDarkMode]
  );

  return (
    <StrictMode>
      <ThemeProvider theme={theme}>
        <CssBaseline enableColorScheme />
        <Box height={"10vh"} marginLeft="20px" alignContent={"center"}>
          <h1>
            <Link href="/" style={{ color: "white", textDecoration: "none" }}>
              Harmony Hootenany
            </Link>
          </h1>
          <LoginLogoutButton />
        </Box>
        <Divider />
        <Box height={"87vh"} sx={{ display: "flex", width: "100vw" }}>
          <script
            src="https://cdn.socket.io/4.6.0/socket.io.min.js"
            integrity="sha384-c79GN5VsunZvi+Q/WObgk2in0CbZsHnjEqvFxC5DxHn9lTfNce2WW6h2pH6u/kF+"
            crossOrigin="anonymous"
          ></script>
          {/*script tag is for websockets to work*/}
          <Routes>
            <Route path="/" element={<RoomSelection />} />
            <Route path="/main" element={<MainPage />} />
            <Route path="/test" element={<SecondPage />} />
            <Route path="/login" element={<AuthForm />} />
          </Routes>
        </Box>
      </ThemeProvider>
    </StrictMode>
  );
}
