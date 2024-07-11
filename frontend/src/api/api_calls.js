import axios from "axios";

import { loginEndpoint, signupEndpoint } from "./endpoints.js";

export const login = async (credentials) => {
  const response = await axios.post(
    loginEndpoint,
    new URLSearchParams({
      username: credentials.username,
      password: credentials.password,
    }),
  );

  return response.data;
};

export const signup = async (credentials) => {
    const response = await axios.post(
        signupEndpoint,
        new URLSearchParams({
        username: credentials.username,
        password: credentials.password,
        email: credentials.email,
        }),
    );

    return response.data;
}
