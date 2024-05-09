import React, {useEffect} from 'react';
import { Link, useNavigate } from 'react-router-dom';

function Navbar(props) {
  const navigate = useNavigate();

  const user = localStorage.getItem('user');

  const handleLogout = async () => {
    localStorage.removeItem('user');
    console.log("logged out ");
    return navigate("/")
    };

  useEffect(() => {
      if (localStorage.getItem('user')) {
        return navigate("/")
      }
  }, [])
  return (
    <nav>
      <ul>
        {user ? (
          <>
            <li><Link to="/edit-profile">Edit Profile</Link></li>
            <li><Link to="/user-feed">User Feed</Link></li>
            <li><Link to="/block-feed">Block Feed</Link></li>
            <li><Link to="/hood-feed">Hood Feed</Link></li>
            <li><Link to="/edit-profile">Edit Profile</Link></li>
            <li><Link to="/friends-list">Friends</Link></li>
            <li><Link to="/neighbors-list">Neighbors</Link></li>

            
            <li><Link to="/login" onClick={handleLogout}>Logout</Link></li>
          </>
        ) : (
          <>
            <li><Link to="/login">Login</Link></li>
            <li><Link to="/register">Register</Link></li>
          </>
        )}
      </ul>
    </nav>
  );
}

export default Navbar;
