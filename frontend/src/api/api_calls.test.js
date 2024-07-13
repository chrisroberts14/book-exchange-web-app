import * as axios from "axios";

import {login, signup, setToken, authHeader, getAllBooks, getAllListings} from "./api_calls.js";

jest.mock("axios");

describe("login api call", () => {
  it("should return user data on success", async () => {
    axios.post.mockResolvedValue({
      data: { username: "test", password: "test" }, status: 200,
    });
    const data = await login({ username: "test", password: "test" });

    expect(data).toStrictEqual({ username: "test", password: "test" });
  });

  it("should return error message when logging in with wrong credentials", async () => {
    axios.post.mockResolvedValue({ status: 401 });
    const data = await login({ username: "test", password: "test" });

    expect(data).toStrictEqual({errorMessage: "Username or password is incorrect" });
  });

  it("should return error message when logging in with empty credentials", async () => {
    const data = await login({ username: "", password: "" });
    expect(data).toStrictEqual({errorMessage: "Username or password is incorrect" });
  });

  it("should return an error when server errors occur", async () => {
    axios.post.mockRejectedValue(new Error("An error has occurred."));
    const data = await login({ username: "test", password: "test" });
    expect(data).toStrictEqual({errorMessage: "An error has occurred." });
  });

});

describe("signup api call", () => {
  it("should return user data on success", async () => {
    axios.post.mockResolvedValue({
      data: {username: "test", email: "test@test.com", id: "test-id"}, status: 201
    });
    const data = await signup({username: "test", password: "test", email: "test@test.com"});
    expect(data).toStrictEqual({username: "test", email: "test@test.com", id: "test-id"});
  });

  it("should return error message when signing up with existing username", async () => {
    axios.post.mockResolvedValue({status: 401});
    const data = await signup({username: "test", password: "test", email: "test@test.com"});
    expect(data).toStrictEqual({errorMessage: "Username already taken"});
  });

  it("should return an error when server errors occur", async () => {
    axios.post.mockRejectedValue(new Error("An error has occurred."));
    const data = await signup({username: "test", password: "test", email: "test@test.com"});
    expect(data).toStrictEqual({errorMessage: "An error has occurred."});
  });
});

describe("setToken", () => {
    it("should set the token", () => {
      setToken("test");
      expect(authHeader()).toStrictEqual({headers: {Authorization: "Bearer test"}});
    });
});

describe("getAllBooks", () => {
  it("should return all books", async () => {
    axios.get.mockResolvedValue({data: [{title: "test", author: "test"}]});
    const data = await getAllBooks();
    expect(data).toStrictEqual([{title: "test", author: "test"}]);
  });

  it("should return an error when server errors occur", async () => {
    axios.get.mockRejectedValue(new Error("An error has occurred."));
    const data = await getAllBooks();
    expect(data).toStrictEqual({errorMessage: "An error has occurred."});
  });
});

describe("getAllListings", () => {
  it("should return all listings", async () => {
    axios.get.mockResolvedValue({data: [{title: "test", author: "test"}]});
    const data = await getAllListings();
    expect(data).toStrictEqual([{title: "test", author: "test"}]);
  });

  it("should return an error when server errors occur", async () => {
    axios.get.mockRejectedValue(new Error("An error has occurred."));
    const data = await getAllListings();
    expect(data).toStrictEqual({errorMessage: "An error has occurred."});
  });
});
