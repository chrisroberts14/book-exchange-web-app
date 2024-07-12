import {useEffect, useState} from "react";

import { NavbarComponent } from "./components/Navbar/Navbar";
import { setToken } from "./api/api_calls";

export function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
     const loggedInUser = window.localStorage.getItem("username");
     const token = window.localStorage.getItem("token");
     if (loggedInUser && token) {
       setUser(loggedInUser);
       setToken(token);
     }
  });

    useEffect(() => {
        const loggedInUser = window.localStorage.getItem("username");
        const token = window.localStorage.getItem("token");
        if (loggedInUser && token) {
            setUser(loggedInUser);
            setToken(token);
        }
    }, [user]);

  return (
    <div>
      <NavbarComponent loggedIn={user} signedIn={false} setUser={setUser} setToken={setToken} user={user}/>
    </div>
  );
}
