import React, { useState } from "react";
import {
  Tabs,
  Tab,
  Input,
  Link,
  Button,
  Card,
  CardBody,
} from "@nextui-org/react";
import{ login, signup } from "../../api/api_calls.js";
import { ErrorMessageBar } from "../ErrorMessageBar/ErrorMessageBar";

export const LoginSignUpForm = ({ setUser, setToken }) => {
  const [formSelected, setFormSelected] = useState("login");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [isError, setIsError] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    const response = await login({username: username, password: password});
    if (response.access_token !== undefined) {
      setUser(response.username);
      setUsername("");
      setEmail("");
      setPassword("");
      window.localStorage.setItem("token", response.access_token);
      window.localStorage.setItem("username", response.username);
    } else {
      setIsError(true);
      setTimeout(() => setIsError(false), 5000);
      setErrorMessage(response.errorMessage);
    }
  }

  const handleSignUp = async (e) => {
    e.preventDefault();
    const response = await signup({username: username, password: password, email: email});
      if (response.username !== undefined) {
        setUser(response.username);
        setUsername("");
        setEmail("");
        setPassword("");
      } else {
        setIsError(true);
        setTimeout(() => setIsError(false), 5000);
        setErrorMessage(response.errorMessage);
      }
  }

  const toggleForm = () => {
    setFormSelected(formSelected === "login" ? "sign-up" : "login")
  }

  return (
    <div className="flex flex-auto w-full">
      <Card className={"max-w-full w-[350px]"} radius={"none"}>
        <ErrorMessageBar message={errorMessage} visible={isError} data-testid="error-bar"/>
        <CardBody className="overflow-hidden">
          <Tabs
            fullWidth
            aria-label="Tabs form"
            selectedKey={formSelected}
            size="md"
            onSelectionChange={setFormSelected}
          >
            <Tab key="login" title="Login" data-testid="login-tab">
             <InputBoxes
                    formSelected={formSelected}
                    setUsername={setUsername}
                    setPassword={setPassword}
                    setEmail={setEmail}
                    onSubmitFunc={handleLogin}
                    buttonText="Login"
                    toggleForm={toggleForm}
                    username={username}
                    password={password}
                    email={email}
                />
            </Tab>
            <Tab key="sign-up" title="Sign up" data-testid="signup-tab">
              <InputBoxes
                  formSelected={formSelected}
                  setUsername={setUsername}
                  setPassword={setPassword}
                  setEmail={setEmail}
                  onSubmitFunc={handleSignUp}
                  buttonText="Sign up"
                  toggleForm={toggleForm}
                  username={username}
                  password={password}
                  email={email}
              />
            </Tab>
          </Tabs>
        </CardBody>
      </Card>
    </div>
  );
};

const InputBoxes = ({ formSelected, username, setUsername, password, setPassword, email, setEmail, onSubmitFunc, buttonText, toggleForm }) => {
  return (<form className="flex flex-col gap-4" onSubmit={onSubmitFunc}>
    <Input
        isRequired
        label="Username"
        placeholder="Enter your username"
        type="username"
        data-testid="username-input"
        value={username}
        onChange={(e) => {
          setUsername(e.target.value)
        }}
    />
    {formSelected === "sign-up" ? <Input
        isRequired
        label="Email"
        placeholder="Enter your email"
        type="email"
        value={email}
        data-testid="email-input"
        onChange={(e) => {setEmail(e.target.value)}}
        hidden={formSelected === "login"}
    /> : null}
    <Input
        isRequired
        label="Password"
        placeholder="Enter your password"
        type="password"
        value={password}
        data-testid="password-input"
        onChange={(e) => {
          setPassword(e.target.value)
        }}
    />
    <p className="text-center text-small">
      {buttonText === "Login" ? "Need to create an account? " : "Already have an account? "}
      <Link size="sm" onPress={toggleForm} data-testid="tab-swap-link">
        {buttonText === "Login" ? "Sign up" : "Login"}
      </Link>
    </p>
    <div className="flex gap-2 justify-end">
      <Button fullWidth color="primary" type="submit" data-testid="submit-button">
        {buttonText}
      </Button>
    </div>
  </form>
  );
}
