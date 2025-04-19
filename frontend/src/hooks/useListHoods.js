// hooks/useLogout.js
import axios from "axios";

const useListHoods = async () => {
  try {
    const res = await axios.get("http://localhost/api/v1/hood/", {
      withCredentials: true,
    });
    return res.data;
  } catch (error) {
    console.error("Error fetching hoods:", error);
    return [];
  }
};

export default useListHoods;
