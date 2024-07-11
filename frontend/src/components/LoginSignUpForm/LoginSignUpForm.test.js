import {fireEvent, render, screen, waitFor} from "@testing-library/react";
import {login, signup} from "../../api/api_calls";
import { LoginSignUpForm } from "./LoginSignUpForm.jsx";

jest.mock("../../api/api_calls");

describe("LoginSignUpForm", () => {
  let setUser;

  beforeEach(() => {
    setUser = jest.fn();
    console.log = jest.fn();
    console.error = jest.fn();
  });

  const tryLogin = async () => {
    render(<LoginSignUpForm setUser={setUser} />);
    fireEvent.click(screen.getByTestId("login-tab"));
    fireEvent.change(screen.getByTestId("login-username"), { target: { value: "test_user" } });
    fireEvent.change(screen.getByTestId("login-password"), { target: { value: "password" } });
    fireEvent.click(screen.getByTestId("login-button"));
  }

  const trySignUp = async () => {
    render(<LoginSignUpForm setUser={setUser} />);
    fireEvent.click(screen.getByTestId("signup-tab"));
    fireEvent.change(screen.getByTestId("signup-username"), { target: { value: "test_user" } });
    fireEvent.change(screen.getByTestId("signup-password"), { target: { value: "password" } });
    fireEvent.change(screen.getByTestId("signup-email"), { target: { value: "test@test.com"}});
    fireEvent.click(screen.getByTestId("signup-button"));
  }

  it("renders correctly", () => {
    const { container } = render(<LoginSignUpForm />);
    expect(container).toMatchSnapshot();
  });

  it("clicking on tabs changes form", async () => {
    render(<LoginSignUpForm setUser={setUser} />);
    fireEvent.click(screen.getByTestId("signup-tab"));
    expect(screen.getByTestId("signup-username")).toBeInTheDocument();
    fireEvent.click(screen.getByTestId("login-tab"));
    expect(screen.getByTestId("login-username")).toBeInTheDocument();
  });

  it("clicking on links changes form", async () => {
    render(<LoginSignUpForm setUser={setUser} />);
    fireEvent.click(screen.getByTestId("signup-link"));
    expect(screen.getByTestId("signup-username")).toBeInTheDocument();
    fireEvent.click(screen.getByTestId("login-link"));
    expect(screen.getByTestId("login-username")).toBeInTheDocument();
  });

  it('should login correctly', async () => {
    login.mockResolvedValue({ username: 'testuser', statusCode: 200 });
    await tryLogin();
    await waitFor(() => expect(setUser).toHaveBeenCalled());
  })

  it('should refuse login when using wrong credentials', async () => {
    login.mockResolvedValue({ statusCode: 401 });
    await tryLogin();
    await waitFor(() => expect(console.error).toHaveBeenCalled());
  })

  it('should refuse login when server error', async () => {
    login.mockImplementation(() => {
      throw new Error();
    });
    await tryLogin();
    await waitFor(() => expect(console.error).toHaveBeenCalled());
  })

  it('should signup properly', async () => {
    signup.mockResolvedValue({username: "test", email: "test@test.com", id: "test-id", statusCode: 201});
    await trySignUp();
    await waitFor(() => expect(setUser).toHaveBeenCalled());
  });

  it('should refuse signup if not 201', async () => {
    signup.mockResolvedValue({ statusCode: 401 });
    await trySignUp();
    await waitFor(() => expect(console.error).toHaveBeenCalled());
  });

  it('should refuse signup when server error', async () => {
    signup.mockImplementation(() => {
      throw new Error();
    });
    await trySignUp();
    await waitFor(() => expect(console.error).toHaveBeenCalled());
  });
});
