import React, { useState } from "react";
import { Modal, Button, Form } from "react-bootstrap";

const ThreadModal = ({ handleCreateThread }) => {
  const [showModal, setShowModal] = useState(false);
  const [newThreadName, setNewThreadName] = useState("");
  const [newMessageName, setNewMessageName] = useState("");
  const [error, setError] = useState(null);

  const onCreate = async () => {
    if (!newThreadName.trim() || !newMessageName.trim()) {
      setError("Thread name and message are required.");
      return;
    }

    const result = await handleCreateThread(newThreadName, newMessageName);

    if (result.success) {
      setShowModal(false);
      setNewThreadName("");
      setNewMessageName("");
      setError(null);
    } else {
      setError(result.error || "Failed to create thread.");
    }
  };

  const onCancel = () => {
    setShowModal(false);
    setNewThreadName("");
    setNewMessageName("");
    setError(null);
  };

  return (
    <>
      <Button variant="success" onClick={() => setShowModal(true)}>
        +
      </Button>
      <Modal show={showModal} onHide={onCancel}>
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
                isInvalid={!!error}
              />
              <Form.Label>Message</Form.Label>
              <Form.Control
                as="textarea"
                rows={4}
                placeholder="Enter Message"
                value={newMessageName}
                onChange={(e) => setNewMessageName(e.target.value)}
                isInvalid={!!error}
              />
              {error && (
                <Form.Control.Feedback type="invalid">
                  {error}
                </Form.Control.Feedback>
              )}
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={onCancel}>
            Cancel
          </Button>
          <Button
            variant="primary"
            onClick={onCreate}
            disabled={!newThreadName.trim() || !newMessageName.trim()}
          >
            Create
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};

export default ThreadModal;
