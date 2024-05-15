import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import RegisterForm from '../components/RegisterForm';

function RegisterPage() {
    const user = localStorage.getItem('user');
    const navigate = useNavigate();

    useEffect(() => {
        if (user) {
            navigate('/');
        }
    }, [user, navigate]);

    return (
        <div id="container">
            <h1>Register</h1>
            <RegisterForm />
        </div>
    );

}

export default RegisterPage;
