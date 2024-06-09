import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { FaUserPlus, FaEye } from 'react-icons/fa';

function NeighborsListPage() {
  const [neighbors, setNeighbors] = useState({ block_neighbors: [], hood_neighbors: [], friendships_list: [], following_ids: [] });
  const [refetchTrigger, setRefetchTrigger] = useState(false);

  useEffect(() => {
    async function fetchNeighborData() {
      try {
        const response = await axios.get('http://0.0.0.0:8000/user/neighbors/', {
          headers: {
            Authorization: `${localStorage.getItem('jwt_token')}`,
          },
        });
        console.log(response.data)

        const { block_neighbors, hood_neighbors, friendships_list, following_list } = response.data;

        const followingIds = following_list.map(f => f.user_id);
        const updatedBlockNeighbors = block_neighbors.map(neighbor => ({
          ...neighbor,
          is_friend: friendships_list.includes(neighbor.user_id),
          is_following: followingIds.includes(neighbor.user_id)
        }));
        const updatedHoodNeighbors = hood_neighbors.map(neighbor => ({
          ...neighbor,
          is_friend: friendships_list.includes(neighbor.user_id),
          is_following: followingIds.includes(neighbor.user_id)
        }));
        const updatedFriendshipsList = friendships_list.map(neighbor => ({
          ...neighbor,
          is_friend: friendships_list.includes(neighbor.user_id),
          is_following: followingIds.includes(neighbor.user_id)
        }));

        setNeighbors({
          block_neighbors: updatedBlockNeighbors,
          hood_neighbors: updatedHoodNeighbors,
          friendships_list: updatedFriendshipsList,
          following_ids: followingIds
        });
      } catch (error) {
        console.error('Failed to fetch user data:', error);
      }
    }

    fetchNeighborData();
  }, [refetchTrigger]);

  const handleAddFriend = async (userId, username) => {
    try {
      await axios.post(`http://0.0.0.0:8000/user/add-friend/`, 
        { user_id: userId },
        {
          headers: {
            Authorization: `${localStorage.getItem('jwt_token')}`,
          },
        }
      );
      console.log(`Successfully added ${username} as a friend`);
      alert(`Successfully sent ${username} a friendship request`);
      setRefetchTrigger(!refetchTrigger);
    } catch (error) {
      console.error(`Failed to add ${userId} as a friend`, error);
      alert(`Failed to add ${userId} as a friend`);
    }
  }

  const handleFollowNeighbor = async (userId, username) => {
    try {
      await axios.post(`http://0.0.0.0:8000/user/follow/`, 
        { user_id: userId },
        {
          headers: {
            Authorization: `${localStorage.getItem('jwt_token')}`,
          },
        }
      );
      setRefetchTrigger(!refetchTrigger);
    } catch (error) {
      console.error(`Failed to follow ${userId}`, error);
      alert(`Failed to follow ${userId}`);
    }
  }

  return (
    <div id="container">
      {neighbors.block_neighbors.length > 0 && (
        <>
          <h2>Block Neighbors</h2>
          <table className="neighbor-table">
            <thead>
              <tr>
                <th>Username</th>
                <th>First Name</th>
                <th>Last Name</th>
                <th>Email</th>
                <th></th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {neighbors.block_neighbors.map((neighbor, index) => (
                <tr key={index}>
                  <td>{neighbor.username}</td>
                  <td>{neighbor.first_name}</td>
                  <td>{neighbor.last_name}</td>
                  <td>{neighbor.email}</td>
                  <td>
                    <FaUserPlus
                      onClick={() => handleAddFriend(neighbor.user_id, neighbor.username)}
                      style={{ cursor: neighbor.is_friend ? 'not-allowed' : 'pointer', color: neighbor.is_friend ? 'gray' : 'black' }}
                    /> 
                  </td>
                  <td>
                    <FaEye
                      onClick={() => handleFollowNeighbor(neighbor.user_id, neighbor.username)}
                      style={{ cursor: neighbor.is_following ? 'not-allowed' : 'pointer', color: neighbor.is_following ? 'gray' : 'black' }}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
      {neighbors.hood_neighbors.length > 0 && (
        <>
          <h2>Hood Neighbors</h2>
          <table className="neighbor-table">
            <thead>
              <tr>
                <th>Username</th>
                <th>First Name</th>
                <th>Last Name</th>
                <th>Email</th>
                <th></th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {neighbors.hood_neighbors.map((neighbor, index) => (
                <tr key={index}>
                  <td>{neighbor.username}</td>
                  <td>{neighbor.first_name}</td>
                  <td>{neighbor.last_name}</td>
                  <td>{neighbor.email}</td>
                  <td>
                    <FaUserPlus
                      onClick={() => handleAddFriend(neighbor.user_id, neighbor.username)}
                      style={{ cursor: neighbor.is_friend ? 'not-allowed' : 'pointer', color: neighbor.is_friend ? 'gray' : 'black' }}
                    />
                  </td>
                  <td>
                    <FaEye
                      onClick={() => handleFollowNeighbor(neighbor.user_id, neighbor.username)}
                      style={{ cursor: neighbor.is_following ? 'not-allowed' : 'pointer', color: neighbor.is_following ? 'gray' : 'black' }}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </div>
  );
}

export default NeighborsListPage;
