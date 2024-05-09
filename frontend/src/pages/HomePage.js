import React, { useEffect, useState } from 'react';
import axios from 'axios';
import HealthStatusDisplay from '../components/healthcheck';

function Home() {
  useEffect(() => {
    async function fetchUserData() {
      let storedUserData = localStorage.getItem('user');

      try {
        const response = await axios.get('http://0.0.0.0:8000/user/me/', {
          headers: {
            Authorization: `${localStorage.getItem('jwt_token')}`,
          },
        });
        console.log('User data:', response.data)
        // Set and store the new user data
        localStorage.setItem('user', JSON.stringify(response.data));
      } catch (error) {
        console.error('Failed to fetch user data:', error);
      }
      
    }

    fetchUserData();
  }, []);
  let userData = JSON.parse(localStorage.getItem('user'));
  return (
    <div>
      <HealthStatusDisplay />
      {userData && (
        <div>
          <h2>User Profile</h2>
          <p><strong>User ID:</strong> {userData.user_id}</p>
          <p><strong>Username:</strong> {userData.user_name}</p>
          <p><strong>Name:</strong> {`${userData.first_name} ${userData.last_name}`}</p>
          <p><strong>Address:</strong> {userData.address.replace("\\", "")}</p>
          <p><strong>Email:</strong> {userData.email.replace("\\", "")}</p>
          <p><strong>Description:</strong> {userData.description}</p>
          <p><strong>Block ID:</strong> {userData.block_id}</p>
          <p><strong>Confirmed:</strong> {userData.confirmed ? 'Yes' : 'No'}</p>
        </div>
      )}
    </div>
  );
}

export default Home;
