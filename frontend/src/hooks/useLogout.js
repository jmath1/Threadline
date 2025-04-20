import { useState } from "react";
import axios from "axios";

// Utility to get CSRF token from cookies
const getCsrfToken = () => {
  const name = "csrftoken";
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return null;
};

const useLogout = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const logout = async () => {
    setLoading(true);
    setError(null);
    try {
      const csrfToken = getCsrfToken();
      await axios.post(
        "http://localhost/api/v1/user/logout/",
        {},
        {
          withCredentials: true,
          headers: {
            "X-CSRFToken": csrfToken || "",
          },
        }
      );
      // Clear user data from local storage
      localStorage.removeItem("user");
      return { error: null };
    } catch (err) {
      console.error("Logout error:", err);
      setError(err);
      return { error: err };
    } finally {
      setLoading(false);
    }
  };

  return { logout, loading, error };
};

export default useLogout;
