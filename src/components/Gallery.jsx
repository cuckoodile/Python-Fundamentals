import React from "react";

import Card from "../components/Card";

export default function Gallery({ users }) {
  return (
    <div className="flex flex-wrap gap-5">
      {users.length > 0 ? (
        users.map((u) => <Card key={u.id} data={u} />)
      ) : (
        <p>No Users yet!</p>
      )}
    </div>
  );
}
