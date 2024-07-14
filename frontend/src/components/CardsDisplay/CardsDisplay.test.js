import {render, screen, waitFor} from '@testing-library/react';
import { CardsDisplay } from './CardsDisplay';

describe("CardsDisplay", () => {
    it('should render', () => {
        render(<CardsDisplay cards={[]} />);
        waitFor(() => expect(screen.getByTestId("cards-display")).toBeInTheDocument());
    });
});
