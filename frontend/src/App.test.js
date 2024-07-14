import {fireEvent, render, screen, waitFor} from "@testing-library/react";
import { App } from "./App.jsx";
import {getAllBooks, getAllListings} from "./api/api_calls.js";

jest.mock("./api/api_calls");

describe("App", () => {
    it('should render', () => {
        render(<App />);
        waitFor(() => expect(screen.getByTestId("page-footer")).toBeInTheDocument());
        waitFor(() => expect(screen.getByTestId("page-navbar")).toBeInTheDocument());
        waitFor(() => expect(screen.getByTestId("not-logged-in-page")).toBeInTheDocument());
    });

    it('should render with user logged in', () => {
        window.localStorage.setItem("username", "test");
        window.localStorage.setItem("token", "test");
        render(<App />);
        waitFor(() => expect(screen.getByTestId("page-footer")).toBeInTheDocument());
        waitFor(() => expect(screen.getByTestId("page-navbar")).toBeInTheDocument());
        waitFor(() => expect(screen.getByTestId("cards-display-page")).toBeInTheDocument());
    });

    it('should change state when book tab is clicked', () => {
        getAllBooks.mockResolvedValue([{title: "test", author: "test", desciption: "test"}]);
        getAllListings.mockResolvedValue({errorMessage: "An error has occurred."});
        window.localStorage.setItem("username", "test");
        window.localStorage.setItem("token", "test");
        render(<App />);
        fireEvent.click(screen.getByTestId("books-tab"));
        waitFor(() => expect(screen.getByTestId("cards-display-page")).toBeInTheDocument());
        waitFor(() => expect(screen.getByTestId("book-card")).toBeInTheDocument());
    });

    it('should change state when listings tab is clicked', () => {
        getAllListings.mockResolvedValue([{title: "test", author: "test", desciption: "test"}]);
        getAllBooks.mockResolvedValue({errorMessage: "An error has occurred."});
        window.localStorage.setItem("username", "test");
        window.localStorage.setItem("token", "test");
        render(<App />);
        fireEvent.click(screen.getByTestId("books-tab"));
        fireEvent.click(screen.getByTestId("listings-tab"));
        waitFor(() => expect(screen.getByTestId("cards-display-page")).toBeInTheDocument());
        waitFor(() => expect(screen.getByTestId("listing-card")).toBeInTheDocument());
    });

    it('should show an error if an error occurs after changing tabs to books', () => {
        getAllListings.mockResolvedValue([{title: "test", author: "test", desciption: "test"}]);
        getAllBooks.mockResolvedValue({errorMessage: "An error has occurred."});
        window.localStorage.setItem("username", "test");
        window.localStorage.setItem("token", "test");
        render(<App />);
        fireEvent.click(screen.getByTestId("books-tab"));
        waitFor(() => expect(screen.getByTestId("error-message")).toBeInTheDocument());
    });

    it('should show an error if an error occurs after changing tabs to listings', () => {
        getAllBooks.mockResolvedValue([{title: "test", author: "test", desciption: "test"}]);
        getAllListings.mockResolvedValue({errorMessage: "An error has occurred."});
        window.localStorage.setItem("username", "test");
        window.localStorage.setItem("token", "test");
        render(<App />);
        fireEvent.click(screen.getByTestId("books-tab"));
        fireEvent.click(screen.getByTestId("listings-tab"));
        waitFor(() => expect(screen.getByTestId("error-message")).toBeInTheDocument());
    });

    it('should show an error if changing tabs to books (not implemented)', () => {
        getAllBooks.mockResolvedValue([]);
        window.localStorage.setItem("username", "test");
        window.localStorage.setItem("token", "test");
        render(<App />);
        fireEvent.click(screen.getByTestId("users-tab"));
        waitFor(() => expect(screen.getByTestId("error-message")).toBeInTheDocument());
    });
});
