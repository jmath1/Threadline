import { useState, useCallback } from "react";
import axios from "axios";
import { useEffect } from "react";

const useMe = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchUser = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get("http://localhost/api/v1/user/me/", {
        withCredentials: true,
      });
      setUser(response.data);
      return response.data;
    } catch (err) {
      console.error("Error fetching user data:", err);
      setError(err);
      setUser(null);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  // Fetch user data on mount
  useEffect(() => {
    fetchUser();
  }, [fetchUser]);

  return { user, loading, error, refetch: fetchUser };
};

export default useMe;
