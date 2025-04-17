import React, { useState, useEffect } from "react";

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [error, setError] = useState(null);
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    // Connect to the WebSocket
    const ws = new WebSocket("ws://localhost/ws/chat/");
    setSocket(ws);

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.message) {
        // Parse the nested JSON string inside the message field
        const parsedMessage = JSON.parse(data.message);
        setMessages((prevMessages) => [...prevMessages, parsedMessage]);
      } else if (data.error) {
        // Handle errors sent by the backend
        setError(data.error);
      }
    };

    ws.onclose = () => {
      console.log("WebSocket disconnected");
    };

    // Send a ping every 30 seconds to keep the connection alive
    const pingInterval = setInterval(() => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: "ping" }));
      }
    }, 30000);

    return () => {
      clearInterval(pingInterval);
      ws.close();
    };
  }, []);

  const sendMessage = () => {
    if (socket && input.trim()) {
      const hoodId = 1; // Replace with the actual hood ID
      socket.send(JSON.stringify({ message: input, hood_id: hoodId }));
      setInput("");
      setError(null); // Clear any previous errors
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      sendMessage();
    }
  };

  return (
    <div>
      <h1>Chat</h1>
      <div
        style={{
          border: "1px solid #ccc",
          padding: "10px",
          height: "300px",
          overflowY: "scroll",
        }}
      >
        {messages.map((msg, index) => (
          <div key={index} style={{ marginBottom: "10px" }}>
            <span style={{ color: "red", fontWeight: "bold" }}>
              {msg.user}:
            </span>{" "}
            <span>{msg.message}</span>
          </div>
        ))}
      </div>
      {error && (
        <div style={{ color: "red", marginTop: "10px" }}>
          <strong>Error:</strong> {error}
        </div>
      )}
      <div style={{ marginTop: "10px" }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type a message..."
          style={{ width: "80%", padding: "5px" }}
        />
        <button
          onClick={sendMessage}
          style={{ padding: "5px 10px", marginLeft: "5px" }}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default Chat;
