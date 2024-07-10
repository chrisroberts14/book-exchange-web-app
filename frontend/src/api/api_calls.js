import axios from 'axios';
import {loginEndpoint} from "./endpoints.js";


export const login = async (credentials) => {
    const response = await axios.post(loginEndpoint, new URLSearchParams({
        'username': credentials.username,
        'password': credentials.password
    }));
    return response.data;
}
