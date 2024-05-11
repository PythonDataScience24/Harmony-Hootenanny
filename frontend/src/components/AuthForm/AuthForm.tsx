import React, { FormEvent, useState } from "react";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import axios, { AxiosError } from "axios";

export default function AuthForm() {
  const [isLoginMode, setIsLoginMode] = useState(true);
  const [message, setMessage] = useState("");

  const handleSubmit = async (
    event: FormEvent<HTMLFormElement>
  ): Promise<void> => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const userDetails = {
      username: data.get("username"),
      password: data.get("password"),
      confirmPassword: data.get("confirmPassword"),
    };

    const url = isLoginMode
      ? "http://localhost:5000/login"
      : "http://localhost:5000/signup";

    // Define an interface for the error response shape
    interface ErrorResponse {
      error: string;
    }

    try {
      const response = await axios.post(url, userDetails);
      console.log("Success:", response.data);

      // Store user data in local storage
      localStorage.setItem(
        "userData",
        JSON.stringify({
          username: userDetails.username,
          //userId: response.data.userId,
        })
      );

      setMessage("Login successful");
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const axiosError = error as AxiosError<ErrorResponse>; // Specify the expected response shape
        if (axiosError.response?.data?.error) {
          setMessage(axiosError.response.data.error);
        } else {
          setMessage("Failed to login. Please try again.");
        }
      } else {
        setMessage("Failed to login. Please try again.");
      }
    }
  };

  const toggleMode = () => {
    setIsLoginMode(!isLoginMode);
    setMessage(""); // Reset message when switching mode
  };

  return (
    <Container component="main" maxWidth="sm">
      <Box
        sx={{
          boxShadow: 3,
          borderRadius: 2,
          px: 4,
          py: 6,
          marginTop: 8,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Typography component="h1" variant="h5">
          {isLoginMode ? "Sign in" : "Sign up"}
        </Typography>
        {message && (
          <Typography color={message.includes("success") ? "success" : "error"}>
            {message}
          </Typography>
        )}
        <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
          <TextField
            margin="normal"
            required
            fullWidth
            id="username"
            label="Username"
            name="username"
            autoComplete="username"
            autoFocus
          />
          <TextField
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            autoComplete="current-password"
          />
          {!isLoginMode && (
            <TextField
              margin="normal"
              required
              fullWidth
              name="confirmPassword"
              label="Confirm Password"
              type="password"
              id="confirmPassword"
              autoComplete="current-password"
            />
          )}
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            {isLoginMode ? "Sign In" : "Sign Up"}
          </Button>
          <Button
            fullWidth
            variant="outlined"
            onClick={toggleMode}
            sx={{ mt: 1, mb: 2 }}
          >
            {isLoginMode
              ? "Create an account"
              : "Already have an account? Sign In"}
          </Button>
        </Box>
      </Box>
    </Container>
  );
}
