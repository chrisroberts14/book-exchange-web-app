import {render, waitFor, screen} from "@testing-library/react";
import {ListingCard} from "./ListingCard.jsx";

describe("ListingCard", () => {
    it('should render', () => {
        render(<ListingCard listing={{title: "test", seller: {username: "test_user"}, price: 1.00, description: "test_desc", listed_data: "10-10-2024"}} />);
        waitFor(() => expect(screen.getByTestId("listing-card")).toBeInTheDocument());
    });
});
