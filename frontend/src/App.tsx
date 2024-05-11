import { Box, Button, Divider, Link } from "@mui/material";
import MainPage from "./components/MainPage/MainPage";
import SecondPage from "./components/SecondPage";
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import { StrictMode, useMemo } from "react";
import useMediaQuery from "@mui/material/useMediaQuery";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import { DARK_THEME } from "./colorthemes";
import LoginButton from "./components/MainPage/LoginButton";
import Login from "./components/AuthForm/AuthForm";

export default function App() {
  const router = createBrowserRouter([
    {
      path: "/",
      element: <MainPage />,
    },
    {
      path: "/test",
      element: <SecondPage />,
    },
    {
      path: "/login",
      element: <Login />,
    },
  ]);
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

  const checkAuthStatus = () => {
    const userData = localStorage.getItem("userData");
    return userData
      ? console.log(JSON.parse(userData))
      : console.log("No user logged in");
  };
  checkAuthStatus();

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
          <LoginButton />
        </Box>
        <Divider />
        <Box height={"87vh"} sx={{ display: "flex", width: "100vw" }}>
          <RouterProvider router={router} />
        </Box>
      </ThemeProvider>
    </StrictMode>
  );
}
