import React, { useState, useEffect } from "react";
import { Button, Link } from "@mui/material";
import { checkAuthStatus, logoutUser } from "./utils/auth";

const LoginLogoutButton: React.FC = () => {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(checkAuthStatus());

  // Logout user and update button text
  const handleLogout = (): void => {
    logoutUser();
    setIsLoggedIn(false);
  };

  return (
    <div style={{ position: "absolute", top: "2rem", right: "2rem" }}>
      {isLoggedIn ? (
        <Button
          variant="contained"
          onClick={handleLogout}
          style={{ backgroundColor: "rebeccapurple" }}
        >
          Logout
        </Button>
      ) : (
        <Button
          variant="contained"
          style={{
            backgroundColor: "rebeccapurple",
            textDecoration: "none",
          }}
        >
          <Link
            href="/login"
            style={{
              textDecoration: "none",
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
