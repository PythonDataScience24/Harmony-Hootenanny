/**
 * Checks if user data exists in localStorage to determine login status
 */
export const checkAuthStatus = (): boolean => {
  const userData = localStorage.getItem("userData");
  // Return true if user is logged in
  if (userData) {
    console.log(JSON.parse(userData));
    return true;
  }
  return false;
};

/**
 * Logs out user by removing user data form localStorage
 */
export const logoutUser = (): void => {
  localStorage.removeItem("userData");
  console.log("User logged out successfully.");
};
