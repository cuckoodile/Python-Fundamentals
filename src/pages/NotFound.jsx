import React from "react";
import { useNavigate } from "react-router";

export default function NotFound() {
  const nav = useNavigate();

  return (
    <div className="min-h-screen bg-slate-950 text-white text-5xl flex flex-col justify-center items-center gap-5 ">
      <p>Page not found!</p>
      <button onClick={() => nav("/")}>Back</button>
    </div>
  );
}
