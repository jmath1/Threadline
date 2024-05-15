import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { FaUserPlus } from 'react-icons/fa';

function NeighborsListPage() {
  const [neighbors, setNeighbors] = useState({ block_neighbors: [], hood_neighbors: [] });

  useEffect(() => {
    async function fetchNeighborData() {
      try {
        const response = await axios.get('http://0.0.0.0:8000/user/neighbors/', {
          headers: {
            Authorization: `${localStorage.getItem('jwt_token')}`,
          },
        });
        setNeighbors(response.data);
      } catch (error) {
        console.error('Failed to fetch user data:', error);
      }
    }
    if (neighbors.block_neighbors.length === 0 && neighbors.hood_neighbors.length === 0) {
      fetchNeighborData();
    }
  }, [neighbors]);

  const handleAddFriend = async (userId) => {
    console.log(`Adding ${userId} as a friend`);
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
                      onClick={() => handleAddFriend(neighbor.user_id)}
                      style={{ cursor: 'pointer' }}
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
                      onClick={() => handleAddFriend(neighbor.user_id)}
                      style={{ cursor: 'pointer' }}
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
