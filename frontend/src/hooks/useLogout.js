// hooks/useLogout.js
import useApi from "./useApi";

const useLogout = () => {
  const { makeRequest, data, loading, error } = useApi();

  const logout = () => {
    makeRequest("/user/logout/", "POST");
  };

  return { logout, data, loading, error };
};

export default useLogout;
