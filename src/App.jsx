import React from "react";
import {Outlet} from "react-router"

export default function App() {
  return (
    <div className="min-h-screen bg-slate-950 text-white text-5xl flex">

      <main className="flex-1 flex *:flex-1">
        <Outlet />
      </main>
    </div>
  );
}
