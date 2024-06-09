import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ThreadForm from '../components/ThreadForm';
import { Link } from 'react-router-dom';

function FeedPage(props) {
  const [threads, setThreads] = useState([]);
  const [includeFollow, setIncludeFollow] = useState(false);
  const [refreshToggle, setRefreshToggle] = useState(false); // Toggle to trigger refresh

  useEffect(() => {
    const fetchThreads = async () => {
      try {
        const response = await axios.get(`http://0.0.0.0:8000/thread/${props.feedType}/`, {
          params: { following: includeFollow },
          headers: { Authorization: `${localStorage.getItem('jwt_token')}` }
        });
        console.log(threads);
        setThreads(response.data.results);

      } catch (error) {
        console.error('Error fetching threads:', error);
      }
    };

    fetchThreads();
  }, [props.feedType, includeFollow, refreshToggle]); // Include refreshToggle in the dependency array

  const handleIncludeFollowChange = (e) => {
    setIncludeFollow(e.target.checked);
  };

  const refreshThreads = () => {
    setRefreshToggle(prev => !prev); // Toggle the refresh trigger
  };
  console.log(threads);

  return (
    <div id="container">
      <h2>Start a new {props.feedType} thread</h2>
      <ThreadForm threadType={props.feedType} refreshThreads={refreshThreads}/>
      <hr/>
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
          {threads.map(thread => (
            <tr key={thread.thread_id}>
              <td><small>{thread.created}</small></td>
              <td><Link to={`/thread/${thread.thread_id}/`}>{thread.title}</Link></td>
              <td><Link to={`/user/${thread.author_username}/`}>{thread.author_username}</Link></td>
            </tr>
          ))}
        </tbody>
      </table>
      <h2>New Messages</h2>
    </div>
  );
}

export default FeedPage;
