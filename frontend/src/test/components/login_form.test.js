import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import LoginForm from '../../components/login_form/login_form';
import { login } from '../../api/api_calls';

jest.mock('../../api/api_calls');

describe('LoginForm', () => {
    let setUsername, setPassword, setUser;

    beforeEach(() => {
        setUsername = jest.fn();
        setPassword = jest.fn();
        setUser = jest.fn();
        console.log = jest.fn();
        console.error = jest.fn();
    });

    test('renders LoginForm and submits login', async () => {
        login.mockResolvedValue({ username: 'testuser' });

        render(
            <LoginForm
                username="testuser"
                setUsername={setUsername}
                password="password"
                setPassword={setPassword}
                user={"sample_user"}
                setUser={setUser}
            />
        );

        // Check initial render
        expect(screen.getByRole('Username')).toBeInTheDocument();
        expect(await screen.getByRole('Password')).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();

        // Simulate user input
        fireEvent.change(await screen.getByRole('Username'), { target: { value: 'testuser' } });
        fireEvent.change(await screen.getByRole('Password'), { target: { value: 'password' } });

        // Simulate form submission
        fireEvent.click(await screen.getByRole('button', { name: /login/i }));

        // Check login function call
        await expect(login).toHaveBeenCalledWith({ username: 'testuser', password: 'password' });

        // Check state updates
        await expect(console.log.mock.calls[1]).toStrictEqual(['Logged in:', "sample_user"]);
        expect(setUser).toHaveBeenCalledWith({ username: 'testuser' });
        expect(setUsername).toHaveBeenCalledWith('');
        expect(setPassword).toHaveBeenCalledWith('');
    });

    test('handles login failure', async () => {
        login.mockRejectedValue(new Error('Login failed'));

        render(
            <LoginForm
                username="testuser"
                setUsername={setUsername}
                password="password"
                setPassword={setPassword}
                user={null}
                setUser={setUser}
            />
        );

        // Simulate form submission
        fireEvent.click(screen.getByRole('button', { name: /login/i }));

        // Check login function call
        await expect(login).toHaveBeenCalledWith({ username: 'testuser', password: 'password' });

        // Check error handling
        expect(String(console.error.mock.calls[0])).toStrictEqual("Error: Login failed");
    });

    /*
    test('setPassword should be called when password input changes', () => {
        render(
            <LoginForm
                username="testuser"
                setUsername={setUsername}
                password="password"
                setPassword={setPassword}
                user={null}
                setUser={setUser}
            />
        );

        const test = screen.getByRole('Password');
        fireEvent.change(screen.getByRole('Password'), { target: { value: 'password' } });
        expect(setPassword).toHaveBeenCalled();
        expect(setPassword).toHaveBeenCalledWith('password');
    });

    test('setUsername should be called when username input changes', () => {
        render(
            <LoginForm
                username="testuser"
                setUsername={setUsername}
                password="password"
                setPassword={setPassword}
                user={null}
                setUser={setUser}
            />
        );

        fireEvent.change(screen.getByRole('Username'), { target: { value: 'testuser' } });
        expect(setUsername).toHaveBeenCalledWith('testuser');
    });*/
});
