import { useState, useEffect } from "react";
import axiosInstance from "../utils/axiosInstance";

const useMe = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchUser = async () => {
    setLoading(true);
    try {
      const response = await axiosInstance.get("/user/me/", {
        withCredentials: true,
      });
      setUser(response.data);
    } catch (err) {
      setError(err);
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUser();
  }, []);

  return { user, loading, error, refetch: fetchUser };
};

export default useMe;
