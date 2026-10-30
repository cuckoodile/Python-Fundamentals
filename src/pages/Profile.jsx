import React from "react";
import { useState } from "react";
import { useNavigate, useParams } from "react-router";
import RetrieveUserAPI from "../api/users/RetrieveUserAPI";

export default function Profile() {
  const { id } = useParams();
  const nav = useNavigate();

  const [user, setUser] = useState({});
  const [error, setError] = useState("");
  const [isLoading, setLoading] = useState(true);

  useState(() => {
    RetrieveUserAPI(id)
      .then(setUser)
      .catch(() => setError(`Error fetching user id ${id}`))
      .finally(() => setLoading(false));
  }, []);

  if (isLoading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>Failed to fetch User ID: {id}</p>;
  }

  return (
    <div className="text-4xl flex justify-center items-center gap-10">
      <img
        src={user.profile}
        alt={user.username}
        className="size-100 rounded-full border-3"
      />

      <div className="flex flex-col gap-5">
        <p>Username: {user.username}</p>
        <p>First Name: {user.first_name}</p>
        <p>Last Name: {user.last_name}</p>
        <p>ID: {user.id}</p>

        <button onClick={() => nav("/")}>Back</button>
      </div>
    </div>
  );
}
