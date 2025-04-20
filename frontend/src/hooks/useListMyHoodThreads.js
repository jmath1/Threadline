import { useState, useEffect } from "react";
import axios from "axios";

const useListMyHoodThreads = (neighborhoodId) => {
  const [threads, setThreads] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!neighborhoodId) return;

    const fetchThreads = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await axios.get(
          `http://localhost/api/v1/thread/hood/${neighborhoodId}/`,
          {
            withCredentials: true,
          }
        );
        setThreads(res.data);
      } catch (err) {
        console.error("Error fetching threads:", err);
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchThreads();
  }, [neighborhoodId]);

  return { threads, loading, error };
};

export default useListMyHoodThreads;
