import React from "react";
import useListPopularThreads from "../hooks/useListPopularThreads"; // Adjust the path as necessary

const AllThreads = () => {
  const {
    popularThreads,
    loading: popularThreadsLoading,
    error: popularThreadsError,
  } = useListPopularThreads();

  const getPopularThreads = () => {
    if (popularThreadsLoading) {
      return <div>Loading...</div>;
    }

    if (popularThreadsError) {
      return <div>Error: {popularThreadsError.message}</div>;
    }

    if (!popularThreads || popularThreads.length === 0) {
      return <div>No popular threads available.</div>;
    }

    return (
      <ul>
        {popularThreads.map((thread) => (
          <li key={thread.id}>{thread.title}</li>
        ))}
      </ul>
    );
  };

  return (
    <div>
      <h1>All Threads</h1>
      <div>
        <h2>Popular Threads</h2>
        {getPopularThreads()}
      </div>
    </div>
  );
};
export default AllThreads;
