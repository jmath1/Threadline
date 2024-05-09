import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function RegisterForm({ onSubmit }) {
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        email: '',
        first_name: '',
        last_name: '',
        description: '',
        photoUrl: '',
        address: ''
    });
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
        setError(''); // Reset the error message on new submission
        try {
          let res = await axios.post('http://0.0.0.0:8000/user/register/', formData);
          localStorage.setItem('jwt_token', res.data.jwt_token);
          navigate('/'); // Redirect on successful registration
        } catch (error) {
          if (error.response) {
            
            setError(JSON.stringify(error.response.data, null, 2) || 'Registration failed.'); // More user-friendly message
          } else {
            setError('Registration failed. Please try again later.');
          }
        }
    };
    return (
        <div>
            {error && <div style={{ color: 'red' }} role="alert">{error}</div>}
        <form onSubmit={handleSubmit} className="container mt-5">        <div className="form-group">
        <label htmlFor="username">Username: </label>
            <input
            type="text"
            className="form-control"
            id="username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
            />
        </div>
        <label htmlFor="password">Password: </label>
        <div className="form-group">
            <input
                type="password"
                className="form-control"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
            />
        </div>
        <div className="form-group">
            <label htmlFor="email">Email: </label>
            <input
            type="email"
            className="form-control"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            />
        </div>
        <div className="form-group">
            <label htmlFor="first_name">First Name: </label>
            <input
            type="text"
            className="form-control"
            id="first_name"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
            />
        </div>
        <div className="form-group">
            <label htmlFor="first_name">Last Name: </label>
            <input
            type="text"
            className="form-control"
            id="last_name"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
            />
        </div>
        <div className="form-group">
            <label htmlFor="address">Address: </label>
            <input
            type="text"
            className="form-control"
            id="address"
            name="address"
            value={formData.address}
            onChange={handleChange}
            />
        </div>
        <div className="form-group">
            <label htmlFor="description">Description: </label>
            <textarea
            className="form-control"
            id="description"
            name="description"
            rows="3"
            value={formData.description}
            onChange={handleChange}
            />
        </div>
        <div className="form-group">
            <label htmlFor="photoUrl">Photo URL: </label>
            <input
            type="url"
            className="form-control"
            id="photoUrl"
            name="photoUrl"
            value={formData.photoUrl}
            onChange={handleChange}
            />
        </div>
        <button type="submit" className="btn btn-primary">Submit</button>
        </form>
        </div>
    );
}

export default RegisterForm;
