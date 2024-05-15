import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ThreadForm from '../components/ThreadForm';
import { Link } from 'react-router-dom';

function FeedPage(props) {
  const [threads, setThreads] = useState([]);
  const [includeFollow, setIncludeFollow] = useState(false);

  useEffect(() => {
    fetchThreads(props.threadType);
  }, []);

  const fetchThreads = async (includeFollow) => {
    try {
      // Make AJAX call to fetch existing threads
      const response = await axios.get(`http://0.0.0.0:8000/thread/${props.feedType}/`, {
        params: {"following": includeFollow},           
        headers: {Authorization: `${localStorage.getItem('jwt_token')}`}});
      setThreads(response.data.results);
      console.log(response.data.results)
    } catch (error) {
      console.error('Error fetching threads:', error);
    }
  };

  const handleIncludeFollowChange = async (e) => {
    setIncludeFollow(e.target.checked);
    fetchThreads(!includeFollow);
  };

  return (
    <div id="container">
      <h2>Start a new {props.feedType} thread</h2>
    
      <ThreadForm threadType={props.feedType}/>
      <br></br>
      <hr></hr>
      <h2>All {props.feedType} Threads</h2>
      <label>
        <input
          type="checkbox"
          checked={includeFollow}
          onChange={handleIncludeFollowChange}
        />
        Include {props.feedType}s I follow
      </label>
      <table>
        <thead>
          <tr>
            <th>Created</th>
            <th>Title</th>
            <th>Author</th>
          </tr>
        </thead>
        <tbody>
          {threads.map((thread) => (
            <tr key={thread.thread_id}>
              <td><small>{thread.created}</small></td>
              <td><Link to={`/thread/${thread.thread_id}/`}>{thread.title}</Link></td>
              <td><Link to={`/user/${thread.author_username}/`}>{thread.author_username}</Link></td>
            </tr>
          ))}
        </tbody>
      </table>
          <br></br>
          <hr></hr>
          <br></br>
      <h2>New Messages</h2>
    </div>
  );
}

export default FeedPage;
