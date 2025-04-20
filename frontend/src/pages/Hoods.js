import React, { useState } from "react";
import useListHoods from "../hooks/useListHoods";
import { Table, Form } from "react-bootstrap";

function Hoods() {
  const { hoods, loading, error } = useListHoods();
  const [searchTerm, setSearchTerm] = useState("");

  // Handle loading state
  if (loading) {
    return <div>Loading...</div>;
  }

  // Handle error state
  if (error) {
    return <div>Error: {error.message}</div>;
  }

  // Handle empty data state
  if (!hoods || hoods.length === 0) {
    return <div>No data available.</div>;
  }

  const filteredHoods = hoods.filter((hood) =>
    hood.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div>
      <h1>Hoods</h1>
      <Form.Group className="mb-3" controlId="search">
        <Form.Control
          type="text"
          placeholder="Search by name"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </Form.Group>
      <div style={{ maxHeight: "500px", overflowY: "auto" }}>
        <Table striped bordered hover size="sm" responsive>
          <thead>
            <tr>
              <th>Name</th>
              <th>Members</th>
            </tr>
          </thead>
          <tbody>
            {filteredHoods.map((hood) => (
              <tr key={hood.id}>
                <td>{hood.name}</td>
                <td>{hood.member_count}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      </div>
    </div>
  );
}

export default Hoods;
