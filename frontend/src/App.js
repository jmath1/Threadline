
import './App.css';

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import RegisterPage from './pages/RegisterPage';
import LoginPage from './pages/LoginPage';
import EditProfilePage from './pages/EditProfilePage';
import HomePage from './pages/HomePage';
import FriendsListPage from './pages/FriendsListPage';
import NeighborsListPage from './pages/NeighborsListPage';
import NavBar from './components/NavBar';
import './styles/navbar.css';
import './styles/table.css';

function App() {

  return (
    <div>
    <Router>
        <NavBar/>
        <Routes>
          <Route path="/" element={<HomePage/>} />
          <Route path="/register" element={<RegisterPage/>} />
          <Route path="/login" element={<LoginPage/>} />
          <Route path="/edit-profile" element={<EditProfilePage />} />
          <Route path="/friends-list"element={<FriendsListPage />}></Route>
          <Route path="/neighbors-list"element={<NeighborsListPage />}></Route>
          
        </Routes>
    </Router>
    </div>
  );
}

export default App;


