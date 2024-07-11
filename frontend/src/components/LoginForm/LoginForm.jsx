import React from "react";
import { login } from "../../api/api_calls";
import { Input } from "@nextui-org/react";
import {EyeFilledIcon} from "../EyeFilledIcon/EyeFilledIcon.jsx";
import {EyeSlashFilledIcon} from "../EyeSlashFilledIcon/EyeSlashFilledIcon.jsx";
import {Button} from "@nextui-org/react";


export const LoginForm = ({username, setUsername, password, setPassword, user, setUser}) => {
    const [isVisible, setIsVisible] = React.useState(false);
    const toggleVisibility = () => setIsVisible(!isVisible);


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
            <Input
                isRequired
                type="username"
                label="Username"
                variant="bordered"
                className="max-w-xs"
            />
            <Input
                isRequired
                label="Password"
                variant="bordered"
                endContent={
                    <button className="focus:outline-none" type="button" onClick={toggleVisibility}>
                        {isVisible ? (
                            <EyeSlashFilledIcon className="text-2xl text-default-400 pointer-events-none" />
                        ) : (
                            <EyeFilledIcon className="text-2xl text-default-400 pointer-events-none" />
                        )}
                    </button>
                }
                type={isVisible ? "text" : "password"}
                className="max-w-xs"
            />
            <Button color="primary" type="submit">Login</Button>
        </form>
    )
}
