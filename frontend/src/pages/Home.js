import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import HealthStatusDisplay from '../components/healthcheck';

function Home() {
  const { isAuthenticated, login } = useAuth();

  return (
    <div>
      <HealthStatusDisplay></HealthStatusDisplay>
      <h1>Home Page</h1>
      {!isAuthenticated ? (
        <button onClick={login}>Log In</button>
      ) : (
        <nav>
          <ul>
            <li><Link to="/user-feed">User Feed</Link></li>
            <li><Link to="/block-feed">Block Feed</Link></li>
            <li><Link to="/hood-feed">Hood Feed</Link></li>
          </ul>
        </nav>
      )}
    </div>
  );
}

export default Home;
