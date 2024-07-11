import {EyeSlashFilledIcon} from "./EyeSlashFilledIcon.jsx";
import { render } from '@testing-library/react';

describe('EyeSlashFilledIcon', () => {
    it('renders correctly', () => {
        const { container } = render(<EyeSlashFilledIcon />);
        expect(container).toMatchSnapshot();
    });
});
