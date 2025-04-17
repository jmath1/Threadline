import useApi from "./useApi";

const useEditUser = () => {
  const { makeRequest, data, loading, error } = useApi();

  const editUserAddress = (newAddress) => {
    console.log("Editing user address:", newAddress);
    makeRequest("/user/edit/", "POST", { address: newAddress });
  };

  return { editUserAddress, data, loading, error };
};

export default useEditUser;
