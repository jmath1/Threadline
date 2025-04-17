import React from "react";
import { Form } from "react-bootstrap";
import useEditUser from "../hooks/useEditUser";
import { useContext } from "react";
import { AuthContext } from "../providers/AuthProvider";

const Profile = () => {
  const { editUserAddress, data, loading, error } = useEditUser();
  const { user } = useContext(AuthContext) || {};

  const handleUserEdit = async (address) => {
    editUserAddress(address);
  };

  return (
    <div>
      Neighborhood: {user.neighborhood}
      <Form
        onSubmit={(e) => {
          e.preventDefault();
          const address = e.target.elements.address.value;
          handleUserEdit(address); // Use the entered address
        }}
      >
        <Form.Group controlId="formAddress">
          <Form.Label>Address</Form.Label>
          <Form.Control
            type="text"
            name="address"
            placeholder="Enter your address"
            defaultValue={user.address} // Pre-fill with user's current address
          />
        </Form.Group>
        <button type="submit" className="btn btn-primary">
          Submit
        </button>
      </Form>
    </div>
  );
};

export default Profile;
