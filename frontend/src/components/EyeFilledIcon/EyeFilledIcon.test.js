import {EyeFilledIcon} from "./EyeFilledIcon.jsx";
import { render } from '@testing-library/react';

describe('EyeFilledIcon', () => {
    it('renders correctly', () => {
        const { container } = render(<EyeFilledIcon />);
        expect(container).toMatchSnapshot();
    });
});
