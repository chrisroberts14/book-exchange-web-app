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

export const LoginSignUpForm = ({ setUser }) => {
  const [formSelected, setFormSelected] = useState("login");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [isError, setIsError] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const user = await login({username: username, password: password});
      if (user.statusCode === 200) {
        setUser(user);
      } else {
        setIsError(true);
        setErrorMessage("Incorrect details");
      }
    } catch (e) {
      setIsError(true);
      setErrorMessage("Error logging in");
    }
  }

  const handleSignUp = async (e) => {
    e.preventDefault();
    try {
      const user = await signup({username: username, password: password, email: email});
        if (user.statusCode === 201) {
            setUser(user);
        } else {
            setIsError(true);
            setErrorMessage("User not created");
        }
    } catch (e) {
      setIsError(true);
      setErrorMessage("Error creating user");
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
              />
            </Tab>
          </Tabs>
        </CardBody>
      </Card>
    </div>
  );
};

const InputBoxes = ({ formSelected, setUsername, setPassword, setEmail, onSubmitFunc, buttonText, toggleForm }) => {
  return (<form className="flex flex-col gap-4" onSubmit={onSubmitFunc}>
    <Input
        isRequired
        label="Username"
        placeholder="Enter your username"
        type="username"
        data-testid="username-input"
        onChange={(e) => {
          setUsername(e.target.value)
        }}
    />
    {formSelected === "sign-up" ? <Input
        isRequired
        label="Email"
        placeholder="Enter your email"
        type="email"
        data-testid="email-input"
        onChange={(e) => {setEmail(e.target.value)}}
        hidden={formSelected === "login"}
    /> : null}
    <Input
        isRequired
        label="Password"
        placeholder="Enter your password"
        type="password"
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
