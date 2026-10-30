import { createBrowserRouter, Outlet } from "react-router";

import App from "../App";
import Dashboard from "../pages/Dashboard";
import Profile from "../pages/Profile";
import NotFound from "../pages/NotFound";

// 1. From: routes.jsx (routes)
// 2. ..        Back
// 3. Current Directory: src
// 4. /pages | Current Directory: pages
// 5. /Dashboard | Imported: Dashboard

const routes = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        index: true,
        element: <Dashboard />,
      },
      {
        // path??
        // index??
        // Dynamic Routing ":"
        path: "profile/:id",
        element: <Profile />,
      },
    ],
  },
  {
    path: "*",
    element: <NotFound />,
  },
]);

export default routes;
