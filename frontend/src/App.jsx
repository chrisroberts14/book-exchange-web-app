import { useState } from "react";

import { NavbarComponent } from "./components/Navbar/Navbar";

export function App() {
  const [user, setUser] = useState(null);

  return (
    <div>
      <NavbarComponent loggedIn={user} signedIn={false} />
    </div>
  );
}
