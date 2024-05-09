import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import HomePage from '../pages/HomePage'


function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');  // State to store the error message

  const navigate = useNavigate();
  const user = localStorage.getItem('user');
  
  const handleLogin = async () => {
    try {
      const loginRes = await axios.post('http://0.0.0.0:8000/user/login/', { username, password }, { withCredentials: true });
      localStorage.setItem('jwt_token', loginRes.data.jwt_token);

    
      const userRes = await axios.get('http://0.0.0.0:8000/user/me/', {
        headers: {
          Authorization: `${loginRes.data.jwt_token}`,
        },
        withCredentials: true,
      });
      console.log("working");
      console.log(userRes.data);
      localStorage.setItem('user', JSON.stringify(userRes.data));
      console.log(JSON.stringify(userRes.data));
      console.log("parsed");
      navigate("/")
      
    } catch (error) {
      console.log(error);
      if (error.response) {
        // Display the error message from the server if available
        setErrorMessage(error.response.data.message || 'Login failed.');
      } else {
        // Generic error message if no response from the server
        setErrorMessage('Login failed. Please check your network connection.');
      }
    }
  };


  const authenticated = localStorage.getItem('user');

  if (authenticated) {
        return navigate("/")
  }

  if (!authenticated) {
    return (
      <div>
        <h2>Login</h2>
        {errorMessage && <div style={{ color: 'red' }}>{errorMessage}</div>}
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
        />
        <button onClick={handleLogin}>Login</button>
      </div>
    );
  } else {
    return <HomePage />
  }
}

export default LoginPage;
