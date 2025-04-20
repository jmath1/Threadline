import React, { useState } from "react";
import useListMyHoodThreads from "../hooks/useListMyHoodThreads";
import useMe from "../hooks/useMe";
import { Form, Accordion, Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import ThreadModal from "../components/ThreadModal";
import axios from "axios";

const MyHoodThreads = () => {
  const { user, loading: userLoading, error: userError } = useMe();
  const {
    threads,
    loading: threadsLoading,
    error: threadsError,
    refetch: refetchThreads,
  } = useListMyHoodThreads(user?.hood);
  const [searchTerm, setSearchTerm] = useState("");

  if (userLoading || threadsLoading) {
    return <div>Loading...</div>;
  }

  if (userError || threadsError) {
    return <div>Error: {userError?.message || threadsError?.message}</div>;
  }

  if (!threads || threads.length === 0) {
    return <div>No data available.</div>;
  }

  const filteredThreads = threads.filter((thread) =>
    thread.name.toLowerCase().includes(searchTerm.toLowerCase())
  );
  const getCsrfToken = () => {
    const name = "csrftoken";
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return null;
  };
  const handleCreateHoodThread = async (threadName, messageContent) => {
    try {
      const response = await axios.post(
        "http://localhost/api/v1/thread/",
        {
          hood: user?.hood,
          name: threadName,
          content: messageContent,
          type: "HOOD",
        },
        {
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
          },
          withCredentials: true,
        }
      );

      const newThread = response.data;
      console.log("Thread created:", newThread);
      refetchThreads(); // Refresh the threads list
      return { success: true, thread: newThread };
    } catch (error) {
      console.error("Error creating thread:", error);
      return { success: false, error: error.message };
    }
  };

  return (
    <div>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <h1>Threads: {user.neighborhood}</h1>
        <ThreadModal handleCreateThread={handleCreateHoodThread} />
      </div>
      <Form.Group className="mb-3" controlId="search">
        <Form.Control
          type="text"
          placeholder="Search by name"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </Form.Group>
      <div style={{ maxHeight: "500px", overflowY: "auto" }}>
        <Accordion defaultActiveKey="0">
          {filteredThreads.map((thread, index) => (
            <Accordion.Item eventKey={index.toString()} key={thread.id}>
              <Accordion.Header>{thread.name}</Accordion.Header>
              <Accordion.Body>
                <p>
                  <strong>Author:</strong> {thread.author.username}
                </p>
                <p>
                  <strong>Created At:</strong>{" "}
                  {new Date(thread.created_at).toLocaleString()}
                </p>
                <p>
                  <strong>Last Message:</strong>{" "}
                  {thread.messages?.length > 0
                    ? new Date(
                        thread.messages[thread.messages.length - 1].created_at
                      ).toLocaleString()
                    : "No messages"}
                </p>
                <p>
                  <strong>Message Count:</strong> {thread.messages?.length || 0}
                </p>
                <Button as={Link} to={`/thread/${thread.id}`} variant="primary">
                  View
                </Button>
              </Accordion.Body>
            </Accordion.Item>
          ))}
        </Accordion>
      </div>
    </div>
  );
};

export default MyHoodThreads;
