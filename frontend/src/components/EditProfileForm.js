import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function EditProfileForm({ onSubmit }) {
    // Retrieve user data from local storage and parse it, or set default values if not present
    const getUserData = () => {
        const storedData = localStorage.getItem('user');
        console.log(storedData)
        return storedData ? JSON.parse(storedData) : {
            username: '',
            password: '',
            email: '',
            first_name: '',
            last_name: '',
            description: '',
            photoUrl: '',
            address: ''
        };
    };

    const [formData, setFormData] = useState(getUserData());
    const [error, setError] = useState(''); // State to hold the error message
    const navigate = useNavigate(); // Hook to navigate programmatically

    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormData(prevState => ({
          ...prevState,
          [name]: value
        }));
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError('');
        try {
          await axios.post('http://0.0.0.0:8000/user/edit/', formData,  {headers: {"Authorization": `${localStorage.getItem('jwt_token')}`}});
          navigate('/');
        } catch (error) {
          if (error.response) {
            setError(JSON.stringify(error.response.data, null, 2) || 'Edit failed.');
          } else {
            setError('Edit failed. Please try again later.');
          }
        }
    };
    return (
        <div>
            {error && <div style={{ color: 'red' }} role="alert">{error}</div>}
            <form onSubmit={handleSubmit} className="container mt-5">
                <div className="form-group">
                    <label htmlFor="username">Username: </label>
                    <input type="text" className="form-control" id="user_name" name="user_name" value={formData.username} onChange={handleChange} required />
                </div>
                <div className="form-group">
                    <label htmlFor="email">Email: </label>
                    <input type="email" className="form-control" id="email" name="email" value={formData.email} onChange={handleChange} required />
                </div>
                <div className="form-group">
                    <label htmlFor="first_name">First Name: </label>
                    <input type="text" className="form-control" id="first_name" name="first_name" value={formData.first_name} onChange={handleChange} />
                </div>
                <div className="form-group">
                    <label htmlFor="last_name">Last Name: </label>
                    <input type="text" className="form-control" id="last_name" name="last_name" value={formData.last_name} onChange={handleChange} />
                </div>
                <div className="form-group">
                    <label htmlFor="address">Address: </label>
                    <input type="text" className="form-control" id="address" name="address" value={formData.address} onChange={handleChange} />
                </div>
                <div className="form-group">
                    <label htmlFor="description">Description: </label>
                    <textarea className="form-control" id="description" name="description" rows="3" value={formData.description} onChange={handleChange} />
                </div>
                <div className="form-group">
                    <label htmlFor="photoUrl">Photo URL: </label>
                    <input type="url" className="form-control" id="photoUrl" name="photoUrl" value={formData.photoUrl} onChange={handleChange} />
                </div>
                <button type="submit" className="btn btn-primary">Submit</button>
            </form>
        </div>
    );
}

export default EditProfileForm;
