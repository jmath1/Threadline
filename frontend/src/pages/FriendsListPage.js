import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { FaTrash, FaUserMinus, FaCheck, FaTimes } from 'react-icons/fa';

function FriendsListPage() {
  const [friends, setFriends] = useState([]);
  const [following, setFollowing] = useState([]);
  const [followers, setFollowers] = useState([]);
  const [friendRequests, setFriendRequests] = useState([]);

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

    async function fetchFriendRequestsData() {
      try {
        const response = await axios.get(`http://0.0.0.0:8000/user/friendship-requests/`, {
          headers: {
            Authorization: `${localStorage.getItem('jwt_token')}`,
          }
        });
        console.log(response.data)
        setFriendRequests(response.data);
      } catch (error) {
        console.error('Failed to fetch friend requests data:', error);
      }
    }

    fetchFriendsData();
    fetchFollowingData();
    fetchFollowersData();
    fetchFriendRequestsData();
  }, []);

  const handleConfirmFriendRequest = async (userId) => {
    try {
      console.log(userId)
      await axios.post(`http://0.0.0.0:8000/user/confirm-friend/`, 
        { user_id: userId },
        {
          headers: {
            Authorization: `${localStorage.getItem('jwt_token')}`,
          }
        }
      );
      setFriendRequests(friendRequests.filter((request) => request.user_id !== userId));
    } catch (error) {
      console.error('Failed to confirm friend request:', error);
    }
  };

  const handleDenyFriendRequest = async (userId) => {
    try {
      await axios.post(`http://0.0.0.0:8000/user/decline-friend/`, 
        { user_id: userId },
        {
          headers: {
            Authorization: `${localStorage.getItem('jwt_token')}`,
          }
        }
      );
      setFriendRequests(friendRequests.filter((request) => request.user_id !== userId));
    } catch (error) {
      console.error('Failed to deny friend request:', error);
    }
  };

  const handleUserRemoval = async (userId, type) => {
    try {
      if (type === 'friends') {
        await axios.post(`http://0.0.0.0:8000/user/delete-friend/`, 
          { user_id: userId },
          {
            headers: {
              Authorization: `${localStorage.getItem('jwt_token')}`,
            }
          }
        );
        setFriends(friends.filter((friend) => friend.user_id !== userId));
      } else if (type === 'following') {
        await axios.post(`http://0.0.0.0:8000/user/follow/`, 
          { user_id: userId },
          {
            headers: {
              Authorization: `${localStorage.getItem('jwt_token')}`,
            }
          }
        );
        setFollowing(following.filter((followee) => followee.user_id !== userId));
      } else if (type === 'followers') {
        console.log(userId);
        await axios.post(`http://0.0.0.0:8000/user/delete-follower/`, 
          { user_id: userId },
          {
            headers: {
              Authorization: `${localStorage.getItem('jwt_token')}`,
            }
          }
        );
        setFollowers(followers.filter((follower) => follower.user_id !== userId));
      }
    } catch (error) {
      console.error(`Failed to remove ${type.slice(0, -1)}:`, error);
    }
  };

  const renderUserTable = (users, tabletype) => (
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
          <tr key={user.user_id}>
            <td><Link to={`/user/${user.user_id}/`}>{user.username}</Link></td>
            <td>{user.block_name}</td>
            <td>{user.hood_name}</td>
            <td>{user.first_name}</td>
            <td>{user.last_name}</td>
            <td><FaUserMinus onClick={() => handleUserRemoval(user.user_id, tabletype)}/></td>
          </tr>
        ))}
      </tbody>
    </table>
  );

  return (
    <div id="container">
      <h2>Friend Requests</h2>
      <div className="friend-requests">
        {friendRequests.map((request) => (
          <div className="friend-request" key={request.user_id}>
            <span>{request.username}</span>
            <button onClick={() => handleConfirmFriendRequest(request.user_id)}>
              <FaCheck />
            </button>
            <button onClick={() => handleDenyFriendRequest(request.user_id)}>
              <FaTimes />
            </button>
          </div>
        ))}
      </div>
      <h2>My Friends</h2>
      {renderUserTable(friends, "friends")}

      <h2>People I'm Following</h2>
      {renderUserTable(following, "following")}

      <h2>My Followers</h2>
      {renderUserTable(followers, "followers")}
    </div>
  );
}

export default FriendsListPage;
