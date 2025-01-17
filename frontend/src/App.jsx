import { useEffect, useState } from "react";
import { NavbarComponent } from "./components/Navbar/Navbar";
import { setToken, getAllBooks, getAllListings } from "./api/api_calls";
import { BookCard } from "./components/BookCard/BookCard.jsx";
import { CardsDisplay } from "./components/CardsDisplay/CardsDisplay.jsx";
import { ErrorMessageBar } from "./components/ErrorMessageBar/ErrorMessageBar.jsx";
import { ListingCard } from "./components/ListingCard/ListingCard.jsx";
import { NotLoggedInPage } from "./components/NotLoggedInPage/NotLoggedInPage.jsx";
import { Footer } from "./components/Footer/Footer.jsx";

export function App() {
  const [user, setUser] = useState(null);
  const [screenState, setScreenState] = useState("listings");
  const [cards, setCards] = useState([]);
  const [isError, setIsError] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
     const loggedInUser = window.localStorage.getItem("username");
     const token = window.localStorage.getItem("token");
     if (loggedInUser && token) {
       setUser(loggedInUser);
       setToken(token);
     } else {
         setToken(null);
     }
  });

  useEffect(() => {
      const loggedInUser = window.localStorage.getItem("username");
      const token = window.localStorage.getItem("token");
      if (loggedInUser && token) {
          setToken(token);
      } else {
          setToken(null);
          setCards([]);
      }
  }, [user]);

    useEffect(() => {
        async function fetchData(){
            switch (screenState) {
                case "books":
                    const books_response = await getAllBooks();
                    if (books_response)
                    {
                        if (books_response.errorMessage !== undefined) {
                            setIsError(true);
                            setTimeout(() => setIsError(false), 5000);
                            setErrorMessage(books_response.errorMessage);
                            return;
                        }
                        setCards(books_response.map((book) => <BookCard key={book.id} book={book}/>));
                    }
                    break;
                case "listings":
                    const listings_response = await getAllListings();
                    if (listings_response){
                        if (listings_response.errorMessage !== undefined) {
                            setIsError(true);
                            setTimeout(() => setIsError(false), 5000);
                            setErrorMessage(listings_response.errorMessage);
                            return;
                        }
                        setCards(listings_response.map((listing) => <ListingCard key={listing.id} listing={listing}/>));
                    }
                    break;
                default:
                    setIsError(true);
                    setTimeout(() => setIsError(false), 5000);
                    setErrorMessage("An error has occurred. (Users are not yet implemented)");
                    setCards([]);
                    break;
            }
        }
        // Make the correct api call generate the cards to be displayed
        fetchData();
    }, [screenState]);

  return (
    <div>
    <NavbarComponent loggedIn={user} setUser={setUser} user={user} screenState={screenState} setState={setScreenState} data-testid="page-navbar"/>
        <ErrorMessageBar message={errorMessage} visible={isError} data-testid="error-message"/>
        {user ? <CardsDisplay cards={cards} data-testid="cards-display-page"/> : <NotLoggedInPage data-testid="not-logged-in-page"/>}
    <Footer data-testid="page-footer"/>
    </div>
  );
}
