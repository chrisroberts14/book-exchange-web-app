import {useEffect, useState} from "react";

import { NavbarComponent } from "./components/Navbar/Navbar";
import { setToken } from "./api/api_calls";
import { BookCard } from "./components/BookCard/BookCard.jsx";
import { CardsDisplay } from "./components/CardsDisplay/CardsDisplay.jsx";

export function App() {
  const [user, setUser] = useState(null);
  const [screenState, setScreenState] = useState("listings");
  const [cards, setCards] = useState([]);

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

    useEffect(() => {
        // Make the correct api call generate the cards to be displayed
        console.log("working");
    }, [screenState]);

  return (
    <div>
      <NavbarComponent loggedIn={user} setUser={setUser} user={user} screenState={screenState} setState={setScreenState}/>
        <div>
            <CardsDisplay cards={cards}/>
        </div>

    </div>
  );
}
