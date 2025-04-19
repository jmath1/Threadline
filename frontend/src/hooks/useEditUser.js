import { useState } from "react";
import axios from "axios";

const useEditUser = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const getCsrfToken = () => {
    const name = "csrftoken";
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return null;
  };

  const editUserAddress = async (address) => {
    setLoading(true);
    try {
      const response = await axios.post(
        "http://localhost/api/v1/user/edit/",
        { address },
        { withCredentials: true, headers: { "X-CSRFToken": getCsrfToken() } }
      );
      setError(null);
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
