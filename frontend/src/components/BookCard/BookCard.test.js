import {render, waitFor, screen} from "@testing-library/react";
import {BookCard} from "./BookCard.jsx";

describe("BookCard", () => {
    it('should render', () => {
        render(<BookCard book={{title: "test", author: "test", isbn: "test"}} />);
        waitFor(() => expect(screen.getByTestId("book-card")).toBeInTheDocument());
    });
});
