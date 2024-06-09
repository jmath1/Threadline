import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const MessageSearch = ({ user_id }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  const handleSearch = async (e) => {
    const query = e.target.value;
    setQuery(query);

    if (query.trim() === '') {
      setResults([]);
      return;
    }

    try {
      const response = await axios.get('http://0.0.0.0:8000/thread/search/', {
        params: { q: query },
        headers: { Authorization: `${localStorage.getItem('jwt_token')}` },
      });

      console.log(response.data);
      setResults(response.data.results);
    } catch (error) {
      console.error('Error searching messages:', error);
      setResults([]);
    }
  };

  return (
    <div id="container">
      <input
        type="text"
        placeholder="Search messages..."
        value={query}
        onChange={handleSearch}
      />
      <ul>
        {results && results.map((result) => (
          <li key={result.title}>
            <strong><Link to={`/thread/${result.thread_id}/`}>{result.title}</Link></strong>
            <div>
            <strong>Message:</strong> {result.title}<br />
            <strong>Created:</strong> {result.datetime}<br />

            <strong>Author:</strong> {result.first_name} {result.last_name}<br />
            </div>
          </li>
              ))}
            </ul>
        
    </div>
  );
};

export default MessageSearch;
