import React from "react";
import { login } from "../../api/api_calls";

type LoginFormProps = {
    username: string,
    setUsername: (username: string) => void,
    password: string,
    setPassword: (username: string) => void
    user: any,
    setUser: (user: any) => void
}

const LoginForm = ({username, setUsername, password, setPassword, user, setUser} : LoginFormProps) => {
    const handleLogin = async (event: { preventDefault: () => void; }) => {
        event.preventDefault();
        console.log('Logging in with:', username, password);
        try {
            const user_login = await login({username, password});
            setUser(user_login);
            setUsername('');
            setPassword('');
            console.log('Logged in:', user);
        } catch (exception) {
            console.error('Login failed:', exception);
        }
    }

    return (
        <form onSubmit={handleLogin}>
            <div>
                username:
                <input
                    type={"text"}
                    value={username}
                    name={"Username"}
                    onChange={({target}) => setUsername(target.value)}
                />
            </div>
            <div>
                password
                <input
                    type="password"
                    value={password}
                    name="Password"
                    onChange={({target}) => setPassword(target.value)}
                />
            </div>
            <button type="submit">login</button>
        </form>
    )
}

export default LoginForm;
