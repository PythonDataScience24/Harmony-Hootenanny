import React from "react";
import { Button, Link } from "@mui/material";
import { useNavigate } from "react-router-dom";

const LoginButton: React.FC = () => {
  return (
    <Button
      variant="contained"
      sx={{
        position: "absolute",
        top: "2rem",
        right: "2rem",
        backgroundColor: "rebeccapurple",
      }}
    >
      <Link href="/login">Login</Link>
    </Button>
  );
};

export default LoginButton;
