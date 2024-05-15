import React, { useState, useEffect } from 'react';

function CreateThreadPage() {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [type, setType] = useState('user');
    const [taggedUsers, setTaggedUsers] = useState([]);
    const [users, setUsers] = useState([]);

    useEffect(() => {
        const fetchUsers = async () => {
            let response;
            switch (type) {
                case 'user':
                    response = await fetch('/user/friends-and-neighbors/');
                    break;
                case 'hood':
                    response = await fetch('/hood/members/');
                    break;
                case 'block':
                    response = await fetch('/block/members/');
                    break;
                default:
                    return;
            }
            const data = await response.json();
            console.log(data);
            setUsers(data);
        };
        fetchUsers();
    }, [type]);

    const handleSubmit = (event) => {
        event.preventDefault();

        const data = { title, description, type, taggedUsers };

        fetch('/thread/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
    };

    return (
        <form onSubmit={handleSubmit}>
            <label>
                Title:
                <input type="text" value={title} onChange={e => setTitle(e.target.value)} />
            </label>
            <label>
                Description:
                <textarea value={description} onChange={e => setDescription(e.target.value)} />
            </label>
            <label>
                <input type="radio" value="user" checked={type === 'user'} onChange={e => setType(e.target.value)} />
                User
            </label>
            <label>
                <input type="radio" value="hood" checked={type === 'hood'} onChange={e => setType(e.target.value)} />
                Hood
            </label>
            <label>
                <input type="radio" value="block" checked={type === 'block'} onChange={e => setType(e.target.value)} />
                Block
            </label>
            <label>
                Tag users:
                <select multiple value={users} onChange={e => setTaggedUsers(Array.from(e.target.selectedOptions, option => option.value))}>
                    {users.map(user => (
                        <option key={user.id} value={user.id}>{user.name}</option>
                    ))}
                </select>
            </label>
            <button type="submit">Submit</button>
        </form>
    );
}

export default CreateThreadPage;