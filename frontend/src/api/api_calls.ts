import axios from 'axios';
import {loginEndpoint} from "./endpoints";

type LoginCredentials = {
    username: string,
    password: string
}

export const login = async (credentials: LoginCredentials) => {
    const response = await axios.post(loginEndpoint, new URLSearchParams({
        'username': credentials.username,
        'password': credentials.password
    }));
    console.log('Login response:', response.data);
    return response.data;
}
