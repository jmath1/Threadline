import { useState } from "react";
import axiosInstance from "../utils/axiosInstance";

const useEditUser = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const editUserAddress = async (address) => {
    setLoading(true);
    try {
      const response = await axiosInstance.post(
        "/user/edit/",
        { address },
        { withCredentials: true }
      );
      return response.data; // Return updated user data
    } catch (err) {
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { editUserAddress, loading, error };
};

export default useEditUser;
