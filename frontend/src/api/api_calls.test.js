import * as axios from "axios";

import { login, signup } from "./api_calls.js";

jest.mock("axios");

describe("login api call", () => {
  it("should return user data on success", async () => {
    axios.post.mockResolvedValue({
      data: { username: "test", password: "test" },
    });
    const data = await login({ username: "test", password: "test" });

    expect(data).toStrictEqual({ username: "test", password: "test" });
  });

  it("should return null on failure", async () => {
    axios.post.mockResolvedValue({ data: null });
    const data = await login({ username: "test", password: "test" });

    expect(data).toBe(null);
  });
});


describe("signup api call", () => {
  it("should return user data on success", async () => {
    axios.post.mockResolvedValue({
      data: {username: "test", email: "test@test.com", id: "test-id"}
    });
    const data = await signup({username: "test", password: "test", email: "test@test.com"});
    expect(data).toStrictEqual({username: "test", email: "test@test.com", id: "test-id"});
  });
});
