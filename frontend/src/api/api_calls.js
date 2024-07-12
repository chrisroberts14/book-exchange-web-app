import axios from "axios";
import {getAllBooksEndpoint, loginEndpoint, signupEndpoint} from "./endpoints.js";

let token = null;

export const setToken = (newToken) => {
    token = `Bearer ${newToken}`;
}

export const authHeader = () => {
    return {
        headers: {
            Authorization: token,
        },
    };
}

export const login = async (credentials) => {
    try {
        if (!credentials.username || !credentials.password) {
            return { errorMessage: "Username or password is incorrect" };
        }
        const response = await axios.post(
            loginEndpoint,
            new URLSearchParams({
                username: credentials.username,
                password: credentials.password,
            }),
        );
        if (response.status !== 200) {
            return {errorMessage: "Username or password is incorrect" };
        } else {
            return response.data;
        }
    } catch (e) {
        return {errorMessage: "An error has occurred." };
    }
};

export const signup = async (credentials) => {
    try{
        const response = await axios.post(
            signupEndpoint,
            {
                username: credentials.username,
                password: credentials.password,
                email: credentials.email,
            },
        );
        if (response.status !== 201) {
            return {errorMessage: "Username already taken" };
        } else {
            return response.data;
        }
    } catch (e) {
        return {errorMessage: "An error has occurred." };
    }
}

export const getAllBooks = async () => {
    const auth = authHeader();
    try {
        const response = await axios.get(
            getAllBooksEndpoint,
            auth,
        );
        return response.data;
    } catch (e) {
        return {errorMessage: "An error has occurred." };
    }
}
