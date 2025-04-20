import { useState, useEffect } from "react";
import axios from "axios";

const useMe = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUser = async () => {
      setLoading(true);
      setError(null);
      try {
        // Check local storage first
        const storedUser = localStorage.getItem("user");
        if (storedUser) {
          setUser(JSON.parse(storedUser));
          setLoading(false);
          return;
        }

        // Fetch from API if not in local storage
        const response = await axios.get("http://localhost/api/v1/user/me/", {
          withCredentials: true,
        });
        setUser(response.data);
        localStorage.setItem("user", JSON.stringify(response.data));
      } catch (err) {
        console.error("Error fetching user data:", err);
        setError(err);
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []); // Empty dependency array to run only once on mount

  return { user, loading, error };
};

export default useMe;
