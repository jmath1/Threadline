import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ThreadForm = (props) => {
  const [formData, setFormData] = useState({
    title: '',
    block_id: null,
    hood_id: null,
    user_id: null,
    threadType: 'UserThread',
    messageBody: '',
    address: ''
  });

  const [friendsList, setFriendsList] = useState([]);

  useEffect(() => {
    fetchFriendsList();
  }, []);

  const fetchFriendsList = async () => {
    try {
      // Make AJAX call to fetch friends list data
      const response = await axios.get('http://0.0.0.0:8000/user/friends/', {headers: {"Authorization": `${localStorage.getItem('jwt_token')}`}});
      console.log("Friends list response:", response.data)
      setFriendsList(response.data.results);
    } catch (error) {
      console.error('Error fetching friends list:', error);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Make AJAX call to create thread
      const response = await axios.post('http://0.0.0.0:8000/thread/create/', formData , {headers: {"Authorization": `${localStorage.getItem('jwt_token')}`}});
      console.log('Thread created:', response.data);
      // Reset form data after successful submission
      setFormData({
        title: '',
        block_id: null,
        hood_id: null,
        user_id: null,
        threadType: 'UserThread',
        messageBody: '',
        address: '' // Reset address field
      });
    } catch (error) {
      console.error('Error creating thread:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Title:
        <input
          type="text"
          name="title"
          value={formData.title}
          onChange={handleChange}
        />
      </label>
      <br />
  
      <br />
      {console.log(props.threadType)}
      {props.threadType === 'user' && (
        <label>
          Select Friend:
          <select name="user_id" value={formData.user_id} onChange={handleChange}>
            <option value="">Select Friend</option>
            {friendsList.map((friend) => (
              <option key={friend.user_id} value={friend.user_id}>
                {friend.username}
              </option>
            ))}
          </select>
        </label>
      )}
      <br />

      <label>
        Message Body:
        <textarea
          name="messageBody"
          value={formData.messageBody}
          onChange={handleChange}
        />
      </label>
      
      <br />

      <label>
        Address:
        <input
          type="text"
          name="address"
          value={formData.address}
          onChange={handleChange}
        />
      </label>
      <br />

      <button type="submit" disabled={!formData.user_id && props.threadType === "user"}>Submit</button>
    </form>
  );
};

export default ThreadForm;
