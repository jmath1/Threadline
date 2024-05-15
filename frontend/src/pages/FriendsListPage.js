import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { FaTrash, FaUserMinus } from 'react-icons/fa';

function FriendsListPage() {
  const [friends, setFriends] = useState([]);
  const [following, setFollowing] = useState([]);
  const [followers, setFollowers] = useState([]);

  console.log(friends);
  console.log(following);
  console.log(followers);

  useEffect(() => {
    async function fetchFriendsData() {
      try {
        const response = await axios.get(`http://0.0.0.0:8000/user/friends/`, {
          headers: {
            Authorization: `${localStorage.getItem('jwt_token')}`,
          },
        });
        setFriends(response.data.results);
      } catch (error) {
        console.error('Failed to fetch friends data:', error);
      }
    }

    async function fetchFollowingData() {
      try {
        const response = await axios.get(`http://0.0.0.0:8000/user/following/`, {
          headers: {
            Authorization: `${localStorage.getItem('jwt_token')}`,
          }
        });
        setFollowing(response.data.results);
      } catch (error) {
        console.error('Failed to fetch following data:', error);
      }
    }

    async function fetchFollowersData() {
      try {
        const response = await axios.get(`http://0.0.0.0:8000/user/followers/`, {
          headers: {
            Authorization: `${localStorage.getItem('jwt_token')}`,
          }
        });
        setFollowers(response.data.results);
      } catch (error) {
        console.error('Failed to fetch followers data:', error);
      }
    }

    fetchFriendsData();
    fetchFollowingData();
    fetchFollowersData();
  }, []);

  const renderUserTable = (users) => (
    <table className="user-table">
      <thead>
        <tr>
          <th>Username</th>
          <th>Block</th>
          <th>Hood</th>
          <th>First Name</th>
          <th>Last Name</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        {users.map((user) => (
          <tr key={user.id}>
            <td><Link to={`/user/${user.user_id}/`}>{user.username}</Link></td>
            <td>{user.block_name}</td>
            <td>{user.hood_name}</td>
            <td>{user.first_name}</td>
            <td>{user.last_name}</td>
            <td><FaUserMinus /></td>
          </tr>
        ))}
      </tbody>
    </table>
  );

  return (
    <div id="container">
      <h2>My Friends</h2>
      {renderUserTable(friends)}

      <h2>People I'm Following</h2>
      {renderUserTable(following)}

      <h2>My Followers</h2>
      {renderUserTable(followers)}
    </div>
  );
}

export default FriendsListPage;
