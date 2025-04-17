import React, { createContext } from "react";
import useMe from "../hooks/useMe";
import axios from "axios";
export const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const { user, loading, error } = useMe();

  const getCsrfToken = () => {
    const cookieValue = document.cookie
      .split("; ")
      .find((row) => row.startsWith("csrftoken="))
      ?.split("=")[1];
    return cookieValue ? decodeURIComponent(cookieValue) : null;
  };

  const handleLoginWithGoogle = () => {
    window.location.href = "http://localhost/auth/login/google-oauth2/";
  };

  const handleLogout = async () => {
    try {
      const csrfToken = getCsrfToken();
      await axios.post(
        "http://localhost/api/v1/user/logout/",
        {},
        {
          headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/json",
          },
          withCredentials: true,
        }
      );
      window.location.reload();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        error,
        handleLoginWithGoogle,
        handleLogout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
