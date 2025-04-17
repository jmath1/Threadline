import React, { createContext, useEffect, useState } from "react";
import useMe from "../hooks/useMe";
import useLogout from "../hooks/useLogout";

export const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const { user: fetchedUser, loading, error, refetch } = useMe(); // Get refetch from useMe
  const { logout, loading: logoutLoading, error: logoutError } = useLogout();
  const [user, setUser] = useState(fetchedUser); // Manage user state locally
  const [loggedOut, setLoggedOut] = useState(false);

  // Sync fetchedUser from useMe to local user state
  useEffect(() => {
    setUser(fetchedUser);
  }, [fetchedUser]);

  const handleLoginWithGoogle = () => {
    window.location.href = "http://localhost/auth/login/google-oauth2/";
  };

  const handleLogout = async () => {
    try {
      logout();
      setLoggedOut(true);
      setUser(null);
    } catch (err) {
      console.error("Logout failed:", err);
    }
  };

  const updateUser = (updatedUser) => {
    setUser(updatedUser);
  };

  useEffect(() => {
    if (loggedOut) {
      window.location.reload();
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
        updateUser, // Expose updateUser function
        refetch, // Expose refetch for manual re-fetching if needed
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
