import React from "react";
import { useState } from "react";
import { useEffect } from "react";

import Gallery from "../components/Gallery";
import ListUsersAPI from "../api/users/ListUsersAPI";
import FormPupop from "../components/FormPupop";

export default function Dashboard() {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState("");
  const [isLoading, setLoading] = useState(true);
  const [isVisible, setVisible] = useState(false);

  useEffect(() => {
    // .then()    Success
    // .catch()   Error
    // .finally() Eitherways

    ListUsersAPI()
      .then(setUsers)
      .catch(() => setError("Failed to fetch Users!"))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="p-4 relative">
      <header className="flex justify-between mb-7 border-b">
        <h1>Users Dashboard</h1>

        <button onClick={() => setVisible(true)}>Create</button>
      </header>

      <Gallery users={users} />

      {isVisible && <FormPupop setVisible={setVisible} />}
    </div>
  );
}
