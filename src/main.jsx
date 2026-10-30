import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import "./index.css";
import routes from "./routes/routes.jsx";
import { RouterProvider } from "react-router";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    {/* Context Providers */}
    <RouterProvider router={routes} />
  </StrictMode>,
);
