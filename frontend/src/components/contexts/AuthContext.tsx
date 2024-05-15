import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import Cookies from "js-cookie";

interface AuthContextType {
  isLoggedIn: boolean;
  login: (userData: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);

  useEffect(() => {
    // Initially check if the user is logged in by checking the cookie
    updateLoginStatus();
  }, []);

  const updateLoginStatus = () => {
    const userData = Cookies.get("userData");
    setIsLoggedIn(!!userData);
  };

  const login = (userData: string) => {
    console.log(isLoggedIn);
    Cookies.set("userData", userData.trim(), { expires: 1 });
    setIsLoggedIn(true);
  };

  const logout = () => {
    console.log(isLoggedIn);

    Cookies.remove("userData");
    setIsLoggedIn(false);
  };

  return (
    <AuthContext.Provider value={{ isLoggedIn, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
