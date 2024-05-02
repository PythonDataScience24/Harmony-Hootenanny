import { Box } from "@mui/material";
import MainPage from "./components/MainPage/MainPage";
import SecondPage from "./components/SecondPage";
import { RouterProvider, createBrowserRouter } from "react-router-dom";

export default function App() {
  const router = createBrowserRouter([
    {
      path: "/",
      element: <MainPage />,
    },{
      path: "/test",
      element: <SecondPage />
    }
  ])
  return (
    <>
      <h1>Harmony Hootenany</h1>
      <Box sx={{ display: "flex", height:"80vh", width:'100vw'}}>          
        <RouterProvider router={router} />
      </Box>
    </>
  );
}

