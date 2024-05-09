import React from 'react';

function FriendsListPage() {
  let userData = localStorage.getItem('user');
  console.log("friends list");
  userData = JSON.parse(userData);

  return (
    <div>

    </div>
  );
}

export default FriendsListPage;
