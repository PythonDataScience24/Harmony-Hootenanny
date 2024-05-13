import React from "react";
import { Button, Link } from "@mui/material";
import { useAuth } from "../contexts/AuthContext";

const LoginLogoutButton: React.FC = () => {
  const { isLoggedIn, logout } = useAuth();

  return (
    <div style={{ position: "absolute", top: "2rem", right: "2rem" }}>
      {isLoggedIn ? (
        <Button
          variant="contained"
          onClick={logout}
          style={{ backgroundColor: "#1769aa", color: "#FFF" }}
        >
          Logout
        </Button>
      ) : (
        <Button
          variant="contained"
          style={{
            backgroundColor: "#1769aa",
            textDecoration: "none",
          }}
        >
          <Link
            href="/login"
            style={{
              textDecoration: "none",
              color: "#FFF",
            }}
          >
            Login
          </Link>
        </Button>
      )}
    </div>
  );
};

export default LoginLogoutButton;
