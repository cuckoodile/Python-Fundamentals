import React from "react";
import { useNavigate } from "react-router";

export default function Card({ data }) {
  const nav = useNavigate()

  return (
    // profile/3
    <div onClick={() => nav(`profile/${data.id}`)} className="w-70 text-3xl flex flex-col gap-2 border rounded-lg">
      <img src={data.profile} alt={data.username} className="h-40 w-full rounded-t-lg" />

      {/* Text Contents */}
      <div className="p-2">
        <p>Username: {data.username}</p>
        <p>First Name: {data.first_name}</p>
        <p>Last Name: {data.last_name}</p>
        <p>ID: {data.id}</p>
      </div>
    </div>
  );
}
