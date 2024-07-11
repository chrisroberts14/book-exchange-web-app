import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";

// @ts-ignore
import { App } from "./App";
import { Provider } from "./provider.tsx";
import "@/styles/globals.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <BrowserRouter>
      <Provider>
          <main className="dark text-foreground bg-background">
              <App/>
          </main>
      </Provider>
    </BrowserRouter>
  </React.StrictMode>,
);