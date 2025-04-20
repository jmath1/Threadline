import React, { useState } from "react";
import useListMyHoodThreads from "../hooks/useListMyHoodThreads";
import useMe from "../hooks/useMe";
import { Modal, Form, Accordion, Button } from "react-bootstrap";
import { Link } from "react-router-dom";

function MyHoodThreads() {
  const { user, loading: userLoading, error: userError } = useMe();
  const [showModal, setShowModal] = useState(false);
  const [newThreadName, setNewThreadName] = useState("");
  const [newMessageName, setNewMessageName] = useState("");
  console.log("user", user);
  const {
    threads,
    loading: threadsLoading,
    error: threadsError,
  } = useListMyHoodThreads(user?.hood);
  const [searchTerm, setSearchTerm] = useState("");

  // Handle loading and error states
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

  const handleCreateThread = () => {
    // Add logic to create a new thread here
    console.log("Creating thread:", newThreadName);
    setShowModal(false);
    setNewThreadName("");
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
        <Button variant="success" onClick={() => setShowModal(true)}>
          +
        </Button>
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
                  {new Date(
                    thread.messages?.[thread.messages.length - 1]?.created_at
                  ).toLocaleString()}
                </p>
                <p>
                  <strong>Message Count:</strong> {thread.messages?.length || 0}
                </p>
                <Button
                  as={Link}
                  to={`/threads/${thread.id}`}
                  variant="primary"
                >
                  View
                </Button>
              </Accordion.Body>
            </Accordion.Item>
          ))}
        </Accordion>
      </div>

      {/* Modal for creating a new thread */}
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Create New Thread</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-3" controlId="newThreadName">
              <Form.Label>Thread Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter thread name"
                value={newThreadName}
                onChange={(e) => setNewThreadName(e.target.value)}
              />
              <Form.Label>Message</Form.Label>
              <Form.Control
                as="textarea"
                rows={4}
                placeholder="Enter Message"
                value={newMessageName}
                onChange={(e) => setNewMessageName(e.target.value)}
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Cancel
          </Button>
          <Button variant="primary" onClick={handleCreateThread}>
            Create
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
}

export default MyHoodThreads;
