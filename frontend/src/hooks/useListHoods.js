// hooks/useLogout.js
import { useState, useEffect } from "react";
import axios from "axios";

const useListHoods = () => {
  const [hoods, setHoods] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchHoods = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await axios.get("http://localhost/api/v1/hood/", {
          withCredentials: true,
        });
        setHoods(res.data);
      } catch (err) {
        console.error("Error fetching hoods:", err);
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchHoods();
  }, []);

  return { hoods, loading, error };
};

export default useListHoods;
