// hooks/useApi.js
import { useState, useCallback } from "react";
import axiosInstance from "../utils/axiosInstance";

const useApi = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const makeRequest = useCallback(
    async (endpoint, method = "GET", body = null) => {
      setLoading(true);
      setError(null);
      try {
        const response = await axiosInstance({
          url: endpoint,
          method,
          data: body,
          withCredentials: true,
        });
        setData(response.data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    },
    []
  );

  return { makeRequest, data, loading, error };
};

export default useApi;
