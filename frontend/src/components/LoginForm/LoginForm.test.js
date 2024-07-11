import {LoginForm} from "./LoginForm.jsx";
import {fireEvent, render, screen, waitFor} from '@testing-library/react';
import { login } from '../../api/api_calls';
import { userEvent } from '@testing-library/user-event';
import {act} from "react";

jest.mock('../../api/api_calls');


describe('LoginForm', () => {
    let setUser;

    beforeEach(() => {
        setUser = jest.fn();
        console.log = jest.fn();
        console.error = jest.fn();
    });

    it('renders correctly', () => {
        const { container } = render(<LoginForm />);
        expect(container).toMatchSnapshot();
    });

    it('Login submits correctly', async () => {
        login.mockResolvedValue({ username: 'test_user' });

        render(
            <LoginForm
                user={"sample_user"}
                setUser={setUser}
            />
        );
        // Simulate user input
        await userEvent.type(screen.getByLabelText('Username'), 'test_user');
        await userEvent.type(screen.getByLabelText('Password'), 'password');

        fireEvent.click(screen.getByTestId('login-button'));

        await waitFor(() => {
            expect(login).toHaveBeenCalledWith({ username: 'test_user', password: 'password' });
        })
    });

    it('Login fails correctly', async () => {
       // For now this is a console.error but in the future this will be a notification
        login.mockImplementation(() => {
           throw new Error();
        });

        render(
            <LoginForm
                user={"sample_user"}
                setUser={setUser}
            />
        );
        // Simulate user input
        await userEvent.type(screen.getByLabelText('Username'), 'test_user');
        await userEvent.type(screen.getByLabelText('Password'), 'password');

        fireEvent.click(screen.getByTestId('login-button'));

        expect(String(console.error.mock.calls[0])).toStrictEqual("Error");
    });

    it('Login fails correctly with empty password and or username', async () => {
        render(
            <LoginForm
                user={"sample_user"}
                setUser={setUser}
            />
        );

        fireEvent.click(screen.getByTestId('login-button'));

        expect(String(console.error.mock.calls[0])).toStrictEqual("Username and password must not be empty");
    });

});
