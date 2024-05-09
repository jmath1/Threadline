import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import EditProfileForm from '../components/EditProfileForm';

function EditProfilePage() {


    return (
        <div>
            <h1>Edit Profile</h1>
            <EditProfileForm />
        </div>
    );

}

export default EditProfilePage;
