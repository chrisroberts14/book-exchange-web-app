import {fireEvent, render, screen, waitFor, act} from "@testing-library/react";
import {login, signup} from "../../api/api_calls";
import { LoginSignUpForm } from "./LoginSignUpForm.jsx";

jest.mock("../../api/api_calls");

describe("LoginSignUpForm", () => {
  let setUser;

  beforeEach(() => {
    setUser = jest.fn();
  });

  const tryLogin = async () => {
    render(<LoginSignUpForm setUser={setUser} />);
    await act(async () => {
      fireEvent.click(screen.getByTestId("login-tab"));
      fireEvent.change(screen.getByTestId("username-input"), {target: {value: "test_user"}});
      fireEvent.change(screen.getByTestId("password-input"), {target: {value: "password"}});
      fireEvent.click(screen.getByTestId("submit-button"));
    });
  }

  const trySignUp = async () => {
    render(<LoginSignUpForm setUser={setUser} />);
    await act(async () => {
      fireEvent.click(screen.getByTestId("signup-tab"));
      fireEvent.change(screen.getByTestId("username-input"), {target: {value: "test_user"}});
      fireEvent.change(screen.getByTestId("password-input"), {target: {value: "password"}});
      fireEvent.change(screen.getByTestId("email-input"), {target: {value: "test@test.com"}});
      fireEvent.click(screen.getByTestId("submit-button"));
    });
  }

  it("renders correctly", () => {
    const { container } = render(<LoginSignUpForm />);
    expect(container).toMatchSnapshot();
  });

  it("clicking on tabs changes form", async () => {
    render(<LoginSignUpForm setUser={setUser} />);
    fireEvent.click(screen.getByTestId("signup-tab"));
    expect(screen.getByTestId("email-input")).toBeInTheDocument();
    fireEvent.click(screen.getByTestId("login-tab"));
    expect(screen.getByTestId("username-input")).toBeInTheDocument();
  });

  it("clicking on links changes form", async () => {
    render(<LoginSignUpForm setUser={setUser} />);
    fireEvent.click(screen.getByTestId("tab-swap-link"));
    expect(screen.getByTestId("email-input")).toBeInTheDocument();
    fireEvent.click(screen.getByTestId("tab-swap-link"));
    expect(screen.getByTestId("username-input")).toBeInTheDocument();
  });

  it('should login correctly', async () => {
    login.mockResolvedValue({ username: 'testuser', access_token: "test" });
    await tryLogin();
    await waitFor(() => expect(setUser).toHaveBeenCalled());
  })

  it('should refuse login when using wrong credentials', async () => {
    login.mockResolvedValue(() => { "Username or password is incorrect"  });
    await tryLogin();
    waitFor(() => expect(screen.getByTestId("error-bar")).toBeInTheDocument());
  })

  it('should refuse login when server error', async () => {
    login.mockResolvedValue(() => { "An error has occurred." });
    await tryLogin();
    waitFor(() => expect(screen.getByTestId("error-bar")).toBeInTheDocument());
  })

  it('should signup properly', async () => {
    signup.mockResolvedValue({username: "test", email: "test@test.com", id: "test-id", statusCode: 201});
    await trySignUp();
    await waitFor(() => expect(setUser).toHaveBeenCalled());
  });

  it('should refuse signup if not 201', async () => {
    signup.mockResolvedValue({ statusCode: 401 });
    await trySignUp();
    waitFor(() => expect(screen.getByTestId("error-bar")).toBeInTheDocument());
  });

  it('should refuse signup when server error', async () => {
    login.mockResolvedValue(() => { "An error has occurred." });
    await trySignUp();
    waitFor(() => expect(screen.getByTestId("error-bar")).toBeInTheDocument(), {timeout: 3000});
  });
});
