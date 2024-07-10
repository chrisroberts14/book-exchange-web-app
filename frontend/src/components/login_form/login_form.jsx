import React from "react";
import { login } from "../../api/api_calls";


const LoginForm = ({username, setUsername, password, setPassword, user, setUser}) => {
    const handleLogin = async (event) => {
        event.preventDefault();
        console.log('Logging in with:', username, password);
        try {
            const user_login = await login({username, password});
            setUser(user_login);
            setUsername('');
            setPassword('');
            console.log('Logged in:', user);
        } catch (exception) {
            console.error(exception);
        }
    }

    return (
        <form onSubmit={handleLogin}>
            <div>
                username:
                <input
                    type={"text"}
                    role={"Username"}
                    value={username}
                    name={"Username"}
                    onChange={e => setUsername(e.target.value)}
                />
            </div>
            <div>
                password:
                <input
                    type="password"
                    role={"Password"}
                    value={password}
                    name="Password"
                    onChange={e => setPassword(e.target.value)}
                />
            </div>
            <button type="submit">login</button>
        </form>
    )
}

export default LoginForm;
