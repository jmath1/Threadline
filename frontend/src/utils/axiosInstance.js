import axios from "axios";

// Helper function to get a cookie by name
const getCookie = (name) => {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return null;
};

const axiosInstance = axios.create({
  baseURL: "http://localhost/api/v1", // Base URL for all API requests
  timeout: 10000, // Timeout after 10 seconds
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
  withCredentials: true,
});

// Request interceptor to add `csrftoken` and `sessionid` from cookies
axiosInstance.interceptors.request.use(
  (config) => {
    const csrfToken = getCookie("csrftoken");
    if (csrfToken) {
      config.headers["X-CSRFToken"] = csrfToken;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (
      error.response &&
      error.response.status === 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;
      console.error("Unauthorized request. Please check your session.");
      window.location.href = "/login";
    }

    return Promise.reject(error);
  }
);

export default axiosInstance;
