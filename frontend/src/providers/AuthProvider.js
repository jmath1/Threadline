import React, { createContext, useEffect, useState } from "react";
import useMe from "../hooks/useMe";
import useLogout from "../hooks/useLogout";

export const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const { user: fetchedUser, loading, error, refetch } = useMe(); // Use the useMe hook
  const { logout, loading: logoutLoading, error: logoutError } = useLogout();
  const [user, setUser] = useState(null); // Local user state

  // Sync local user state with fetched user data
  useEffect(() => {
    setUser(fetchedUser);
  }, [fetchedUser]);

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
      setUser(null); // Clear user state
      await refetch(); // Refetch to confirm logout (should return null user)
    } catch (err) {
      console.error("Unexpected error during logout:", err);
    }
  };

  const updateUser = (updatedUser) => {
    setUser(updatedUser);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        handleLoginWithGoogle,
        handleLogout,
        logoutLoading,
        logoutError,
        loading, // Expose loading state from useMe
        error, // Expose error state from useMe
        updateUser,
        refetch,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
