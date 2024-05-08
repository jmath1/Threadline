import React, { useState, useEffect } from 'react';
import { fetchHealthStatus } from '../api/healthcheck';

function HealthStatusDisplay() {
  const [healthStatus, setHealthStatus] = useState('Loading...');

  useEffect(() => {
    fetchHealthStatus()
      .then(data => {
        setHealthStatus(data); // Set the response body as the health status
      })
      .catch(error => {
        setHealthStatus('Failed to fetch health status.');
      });
  }, []);

  return (
    <div>
      <h1>Health Status</h1>
      <p>{healthStatus}</p>
    </div>
  );
}

export default HealthStatusDisplay;
