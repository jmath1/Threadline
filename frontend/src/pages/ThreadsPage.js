import React, { useEffect, useState } from 'react';
import axios from 'axios';

function ThreadsPage() {
    const [threads, setThreads] = useState([]);
    const [selectedThread, setSelectedThread] = useState(null);
    const user = JSON.parse(localStorage.getItem("user"));


    useEffect(() => {
      async function fetchNeighborData() {
        try {
          let hood_id = JSON.parse(localStorage.getItem("user")).hood_id;
          const response = await axios.get(`http://0.0.0.0:8000/thread/hood/${hood_id}/`, {
            headers: {
              Authorization: `${localStorage.getItem('jwt_token')}`,
            },
          });
          setThreads(response.data);
        } catch (error) {
          console.error('Failed to fetch user data:', error);
        }
    }
    fetchNeighborData();
      
    }, [threads]);

    const selectThread = (thread) => {
        setSelectedThread(thread);
    };

    const editMessage = (message) => {
        // Implement your message editing logic here
    };

    return (
        <div style={{ display: 'flex' }}>
            Threads page here

            
            <div>
                {threads.map(thread => (
                    <div key={thread.id} onClick={() => selectThread(thread)}>
                        {thread.title}
                    </div>
                ))}
            </div>
            {selectedThread && (
                <div>
                    <h2>{selectedThread.title}</h2>
                    {selectedThread.messages.map(message => (
                        <div key={message.id}>
                            <p>{message.content}</p>
                            {message.author_id === user.id && (
                                <button onClick={() => editMessage(message)}>Edit</button>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default ThreadsPage;