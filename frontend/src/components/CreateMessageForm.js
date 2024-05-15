import React, { useState, useEffect } from 'react';
import axios from 'axios';

const CreateMessageForm = (props) => {
    const [formData, setFormData] = useState({
        body: '',
        address: ''
      });
    
      const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
      };
    
      const handleSubmit = async (e) => {
        e.preventDefault();
        try {
          // Make AJAX call to create thread
          const response = await axios.post(
            'http://0.0.0.0:8000/thread/message/',
            {
              ...formData,
              thread_id: props.threadId // Use thread_id from props
            },
            {
              headers: { Authorization: `${localStorage.getItem('jwt_token')}` }
            }
          );
          console.log('Thread created:', response.data);
          // Reset form data after successful submission
          setFormData({ body: '', address: '' });
        } catch (error) {
          console.error('Error creating thread:', error);
        }
        };
    
      return (
        <form onSubmit={handleSubmit}>
          <label>
            Body:
            <textarea
              name="body"
              value={formData.body}
              onChange={handleChange}
              required
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
              required
            />
          </label>
          <br />
          <button type="submit">Submit</button>
        </form>
      );
};

export default CreateMessageForm;
