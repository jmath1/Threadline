
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
import CreateThreadPage from './pages/CreateThreadPage';
import './styles/navbar.css';
import './styles/table.css';
import FeedPage from './pages/FeedPage';
import ThreadViewPage from './pages/ThreadViewPage';
import UserDetailPage from './pages/UserDetailPage';
import SearchPage from './pages/SearchPage';
import 'leaflet/dist/leaflet.css';

function App() {

  return (
    <div>
<link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />

    <Router>
        <NavBar/>
        <Routes>
          <Route path="/" element={<HomePage/>} />
          <Route path="/register" element={<RegisterPage/>} />
          <Route path="/login" element={<LoginPage/>} />
          <Route path="/edit-profile" element={<EditProfilePage />} />
          <Route path="/search/" element={<SearchPage />} />
          <Route path="/user/:user_id/" element={<UserDetailPage />} />
          <Route path="/friends-list"element={<FriendsListPage />}></Route>
          <Route path="/neighbors-list"element={<NeighborsListPage />}></Route>
          <Route path="/user-feed"element={<FeedPage feedType={"user"}/>}></Route>
          <Route path="/hood-feed"element={<FeedPage feedType={"hood"}/>}></Route>
          <Route path="/block-feed"element={<FeedPage feedType={"block"}/>}></Route>
          <Route path="/create/thread"element={<CreateThreadPage/>}></Route>
          <Route path="thread/:thread_id/"element={<ThreadViewPage />}></Route>
          <Route path="/thread/:thread_id/" element={<ThreadViewPage />} />

        </Routes>
    </Router>
    </div>
  );
}

export default App;


