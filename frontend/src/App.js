
import './App.css';

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';  // Make sure the path matches where your Home component is located
//import UserFeed from './pages/UserFeed';
//import BlockFeed from './pages/BlockFeed';
//import HoodFeed from './pages/HoodFeed';
import { AuthProvider } from './context/AuthContext';  // Assuming AuthContext is set up as explained earlier

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;
