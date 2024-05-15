import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

function UserDetailPage() {
  const { user_id } = useParams(); // Retrieve user_id from route params
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetchUserData(user_id); // Pass user_id to fetchUserData
  }, [user_id]);

  const fetchUserData = async (userId) => {
    try {
      const response = await axios.get(`http://0.0.0.0:8000/user/${userId}/`, {
        headers: { Authorization: `${localStorage.getItem('jwt_token')}` }
      });
      setUser(response.data.results[0]);
    } catch (error) {
      console.error('Error fetching user:', error);
    }
  };
  const renderUserDetails = () => {
    if (!user) return null;
    return (
      <div className="user-details">
        <h2>User Details</h2>
        <p>Username: {user.username}</p>
        <p>First Name: {user.first_name}</p>
        <p>Last Name: {user.last_name}</p>
        <p>Email: {user.email}</p>
        <p>Block Name: {user.block_name}</p>
        <p>Hood Name: {user.hood_name}</p>
        <p>Followers Count: {user.followers_count}</p>
        <p>Following Count: {user.following_count}</p>
        <p>Friends Count: {user.friends_count}</p>
      </div>
    );
  };

  return (
    <div id="container">
      {renderUserDetails()}
    </div>
  );
}

export default UserDetailPage;
