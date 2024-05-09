import React, { useEffect, useState } from 'react';
import axios from 'axios';

function NeighborsListPage() {
  const [neighbors, setNeighbors] = useState([]);

  useEffect(() => {
    async function fetchNeighborData() {
      try {
        const response = await axios.get('http://0.0.0.0:8000/users/neighbors/', {
          headers: {
            Authorization: `${localStorage.getItem('jwt_token')}`,
          },
        });
        setNeighbors(response.data["results"]); // Set neighbors to state
      } catch (error) {
        console.error('Failed to fetch user data:', error);
      }
    }

    fetchNeighborData();
  }, []);

  return (
    <div>
      <h2>Neighbors</h2>
      <table className="neighbor-table">
      <thead>
        <tr>
          <th>Username</th>
          <th>First Name</th>
          <th>Last Name</th>
          <th>Email</th>
        </tr>
      </thead>
      <tbody> 
          {neighbors.map((neighbor, index) => (
            <tr key={index}>
              <td>{neighbor.username}</td>
              <td>{neighbor.first_name}</td>
              <td>{neighbor.last_name}</td>
              <td>{neighbor.email}</td>
            </tr>
          ))}
      </tbody>
      </table>
    </div>
  );
}

export default NeighborsListPage;
