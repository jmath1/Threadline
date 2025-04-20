import { useState, useEffect } from "react";
import axios from "axios";

const useListPopularThreads = () => {
  const [popularThreads, setPopularThreads] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPopularThreads = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await axios.get("http://localhost/api/v1/thread/popular/", {
          withCredentials: true,
        });
        setPopularThreads(res.data);
      } catch (err) {
        console.error("Error fetching popular threads:", err);
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchPopularThreads();
  }, []);

  return { popularThreads, loading, error };
};

export default useListPopularThreads;
