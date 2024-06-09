import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import CreateMessageForm from '../components/CreateMessageForm';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';

import 'leaflet/dist/leaflet.css';  // Make sure to import Leaflet's CSS

const ThreadViewPage = () => {
  const [thread, setThread] = useState(null);
  const { thread_id } = useParams();

  const deleteMessage = async (messageId) => {
    try {
      await axios.delete(`http://0.0.0.0:8000/thread/message/${messageId}/delete/`, {
        headers: {
          Authorization: `${localStorage.getItem('jwt_token')}`,
        },
      });
      // Optionally refetch the thread or update the state to remove the deleted message
      setThread((prevThread) => ({
        ...prevThread,
        messages: prevThread.messages.filter((msg) => msg.message_id !== messageId),
      }));
    } catch (error) {
      console.error('Error deleting message:', error);
    }
  };
  const handleEdit = (messageId) => {
    
  }

  useEffect(() => {
    const fetchThread = async () => {
      try {
        const response = await axios.get(`http://0.0.0.0:8000/thread/${thread_id}`, {
          headers: {
            Authorization: `${localStorage.getItem('jwt_token')}`,
          },
        });
        console.log("Fetched thread data:", response.data); // Check the structure here
        if (response.data.results && response.data.results.messages) {
          setThread(response.data.results);
        } else {
          console.log("No messages in thread data:", response.data);
        }
      } catch (error) {
        console.error('Error fetching thread:', error);
      }
    };

    fetchThread();
  }, [thread_id]);

  if (!thread) {
    return <div>Loading...</div>;
  }

  const icon = L.icon({
    iconUrl: 'http://mt.googleapis.com/vt/icon/name=icons/spotlight/spotlight-poi.png',
    iconSize: [25, 41],
    iconAnchor: [12.5, 41],
    popupAnchor: [0, -41],
  });

  const defaultPosition = thread.messages && thread.messages.length > 0
    ? [thread.messages[0].latitude, thread.messages[0].longitude]
    : [51.505, -0.09];  // Default fallback coordinates

  return (
    <div id="container">
      <h2>Thread Details:</h2>
      <CreateMessageForm thread_id={thread_id} />
      <hr />
      <h3>Messages</h3>
      <ul>
        {thread.messages && thread.messages.map((message) => (
          <li key={message.message_id} className="message-item">
            <div className="message-buttons">
              <button onClick={() => handleEdit(message.message_id)}>Edit</button>
              <button onClick={() => deleteMessage(message.message_id)}>Delete</button>
            </div>
            <strong>Created:</strong> {message.datetime}<br />
            <strong>Author:</strong> {message.username}<br />
            <strong>Body:</strong> {message.body}
          </li>
        ))}
      </ul>
      {thread.messages && (
        <MapContainer id="map" center={defaultPosition} zoom={13}>
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {thread.messages.map((message, idx) => (
            <Marker 
              key={idx} 
              position={[message.latitude, message.longitude]} // Corrected order here
              icon={icon}
            >
              <Popup>
                A message from {message.user_id}: {message.body}
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      )}
    </div>
  );
};

export default ThreadViewPage;
