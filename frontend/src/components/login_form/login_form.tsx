import React from "react";

type LoginFormProps = {
    username: string,
    setUsername: (username: string) => void,
    password: string,
    setPassword: (username: string) => void
}

const Login_Form = ({username, setUsername, password, setPassword} : LoginFormProps) => {
    const handleLogin = (event: { preventDefault: () => void; }) => {
        event.preventDefault();
        console.log('Logging in with:', username, password);
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

export default Login_Form;
export type {LoginFormProps};
