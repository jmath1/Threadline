import React, { useContext, useEffect, useState } from "react";
import { Form } from "react-bootstrap";
import useEditUser from "../hooks/useEditUser";
import { AuthContext } from "../providers/AuthProvider";

const Profile = () => {
  const {
    editUserAddress,
    loading: editLoading,
    error: editError,
  } = useEditUser();
  const { user, refetch } = useContext(AuthContext);
  const [localUser, setLocalUser] = useState(user);

  // Sync localUser with the user from AuthContext
  useEffect(() => {
    setLocalUser(user);
  }, [user]);

  if (!localUser) {
    return <div>Loading user information...</div>;
  }

  const handleUserEdit = async (address) => {
    try {
      await editUserAddress(address); // Perform the edit operation
      await refetch(); // Re-fetch user data to trigger re-render
    } catch (err) {
      console.error("Failed to edit user:", err);
    }
  };

  return (
    <div>
      Neighborhood: {localUser.neighborhood}
      <Form
        onSubmit={(e) => {
          e.preventDefault();
          const address = e.target.elements.address.value;
          handleUserEdit(address); // Trigger user edit
        }}
      >
        <Form.Group controlId="formAddress">
          <Form.Label>Address</Form.Label>
          <Form.Control
            type="text"
            name="address"
            placeholder="Enter your address"
            defaultValue={localUser.address} // Pre-fill with current address
          />
        </Form.Group>
        <button
          type="submit"
          className="btn btn-primary"
          disabled={editLoading} // Disable button while loading
        >
          {editLoading ? "Submitting..." : "Submit"}
        </button>
      </Form>
      {editError && (
        <div className="text-danger">Error: {editError.message}</div>
      )}
    </div>
  );
};

export default Profile;
