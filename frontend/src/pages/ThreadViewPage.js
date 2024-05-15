import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import CreateMessageForm from '../components/CreateMessageForm';

const ThreadViewPage = () => {
  const [thread, setThread] = useState(null);
  const { thread_id } = useParams();

  useEffect(() => {
    const fetchThread = async () => {
      try {
        const response = await axios.get(`http://0.0.0.0:8000/thread/${thread_id}/`, {
            headers: {
              Authorization: `${localStorage.getItem('jwt_token')}`,
            },
          });
        console.log(response.data.results)
        setThread(response.data.results);
      } catch (error) {
        console.error('Error fetching thread:', error);
      }
    };

    fetchThread();

  }, [thread_id]);

  if (!thread) {
    return <div>Loading...</div>;
  }

  return (
    <div id="container">
      <h2>Thread Detais:</h2>
      <CreateMessageForm thread_id={thread_id}></CreateMessageForm>
        <hr></hr>
        <strong>Title:</strong> {thread.title}<br />
      <h3>Messages</h3>

      <ul>
        {thread == [] && thread.messages.map((message) => (
          <li key={message.message_id}>
            <strong>Created:</strong> {message.created}<br />
            <strong>Author:</strong> {message.user_id}<br />
            <strong>Coordinates:</strong> {message.coords}<br />
            <strong>Body:</strong> {message.body}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ThreadViewPage;
