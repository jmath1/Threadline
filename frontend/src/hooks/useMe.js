import useApi from "./useApi";

const useMe = () => {
  const { data, loading, error } = useApi("/user/me", "GET", null, []);

  return { user: data, loading, error };
};

export default useMe;
