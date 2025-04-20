import React, { createContext, useEffect, useState } from "react";
import useMe from "../hooks/useMe";
import useLogout from "../hooks/useLogout";

export const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const { user } = useMe();
  const { logout, loading: logoutLoading, error: logoutError } = useLogout();
  const handleLoginWithGoogle = () => {
    window.location.href = "http://localhost/auth/login/google-oauth2/";
  };

  const handleLogout = async () => {
    try {
      const { error } = await logout();
      if (error) {
        console.error("Logout failed:", error);
        return;
      }
    } catch (err) {
      console.error("Unexpected error during logout:", err);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
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
