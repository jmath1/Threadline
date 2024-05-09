import React from 'react';

function NeighborsListPage() {
  let userData = localStorage.getItem('user');
  console.log("neighbors list");
  userData = JSON.parse(userData);

  return (
    <div>

    </div>
  );
}

export default NeighborsListPage;
