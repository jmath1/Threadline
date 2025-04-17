import React, { createContext, useEffect, useState } from "react";
import axios from "axios";

export const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        setLoading(true);
        const response = await axios.get("http://localhost/api/v1/user/me/", {
          withCredentials: true,
        });
        console.log(response.data);
        setUser(response.data);
        setError(null);
      } catch (err) {
        if (err.response?.status !== 401) {
          setError(err.response?.data?.detail || err.message);
        }
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

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
      setLoading(true);
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
      setUser(null);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
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
