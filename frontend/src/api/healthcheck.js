const apiUrl = 'http://0.0.0.0:8000'; // Adjust the API URL accordingly

export const fetchHealthStatus = async () => {
  try {
    const response = await fetch(`${apiUrl}/healthcheck`);
    if (!response.ok) {
      throw new Error('Network response was not ok.');
    }
    const data = await response.text(); // Assuming the API returns plain text
    return data;
  } catch (error) {
    console.error('There was a problem with the fetch operation:', error);
    throw error;
  }
};
