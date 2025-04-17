import React, { createContext, useEffect, useState } from "react";
import useMe from "../hooks/useMe";
import useLogout from "../hooks/useLogout";

export const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const { user, loading, error } = useMe();
  const { logout, loading: logoutLoading, error: logoutError } = useLogout();
  const [loggedOut, setLoggedOut] = useState(false);

  const handleLoginWithGoogle = () => {
    window.location.href = "http://localhost/auth/login/google-oauth2/";
  };

  const handleLogout = async () => {
    try {
      logout();
      setLoggedOut(true);
    } catch (err) {
      console.error("Logout failed:", err);
    }
  };

  useEffect(() => {
    if (loggedOut) {
      window.location.reload(); // or redirect to login
    }
  }, [loggedOut]);

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        error,
        handleLoginWithGoogle,
        handleLogout,
        logoutLoading,
        logoutError,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
