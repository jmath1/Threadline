import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ThreadForm = (props) => {
  const [formData, setFormData] = useState({
    title: '',
    block_id: null,
    hood_id: null,
    user_id: '',
    threadType: null,
    messageBody: '',
    address: ''
  });

  const [friendsList, setFriendsList] = useState([]);
  const [userInfo, setUserInfo] = useState({ block_id: null, hood_id: null });

  useEffect(() => {
    fetchFriendsList();
    fetchUserInfo();
  }, []);

  const fetchFriendsList = async () => {
    try {
      const response = await axios.get('http://0.0.0.0:8000/user/friends/', {
        headers: { Authorization: `${localStorage.getItem('jwt_token')}` }
      });
      console.log("Friends list response:", response.data);
      setFriendsList(response.data.results);
    } catch (error) {
      console.error('Error fetching friends list:', error);
    }
  };

  const fetchUserInfo = async () => {
    try {
      const response = await axios.get('http://0.0.0.0:8000/user/me/', {
        headers: { Authorization: `${localStorage.getItem('jwt_token')}` }
      });
      setUserInfo({ block_id: response.data.block_id, hood_id: response.data.hood_id });
    } catch (error) {
      console.error('Error fetching user info:', error);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    fetchUserInfo()
    e.preventDefault();
    console.log(formData)
    let dataToSend = { ...formData };
    if (formData.threadType === 'blockThread') {
      dataToSend.block_id = userInfo.block_id;
    } else if (formData.threadType === 'hoodThread') {
      dataToSend.hood_id = userInfo.hood_id;
    } else if (formData.threadType === 'userThread') {
      dataToSend.user_id = formData.userId;
    }

    try {
      await axios.post('http://0.0.0.0:8000/thread/create/', dataToSend, {
        headers: { Authorization: `${localStorage.getItem('jwt_token')}` }
      });
      
      setFormData({
        title: '',
        block_id: null,
        hood_id: null,
        user_id: '',
        threadType: props.threadType,
        messageBody: '',
        address: ''
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
  
      <label>
        Thread Type:
        <select name="threadType" value={formData.threadType} onChange={handleChange}>
          <option value="blockThread">Block Thread</option>
          <option value="hoodThread">Hood Thread</option>
          <option value="userThread">User Thread</option>
        </select>
      </label>
      <br />
  
      {formData.threadType === 'userThread' && (
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

      <button type="submit" disabled={!formData.user_id && formData.threadType === 'userThread'}>Submit</button>
    </form>
  );
};

export default ThreadForm;
