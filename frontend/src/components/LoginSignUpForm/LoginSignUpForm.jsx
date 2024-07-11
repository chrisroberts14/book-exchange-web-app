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

export const LoginSignUpForm = ({ setUser }) => {
  const [formSelected, setFormSelected] = useState("login");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const user = await login({username: username, password: password});
      if (user.statusCode === 200) {
        setUser(user);
      } else {
        console.error("Incorrect details")
      }
    } catch (e) {
      console.error("Error logging in")
    }
  }

  const handleSignUp = async (e) => {
    e.preventDefault();
    try {
      const user = await signup({username: username, password: password, email: email});
        if (user.statusCode === 201) {
            setUser(user);
        } else {
            console.error("User not created")
        }
    } catch (e) {
      console.error("Error creating user")
    }
  }

  return (
    <div className="flex flex-col w-full">
      <Card className="max-w-full w-[340px] h-[400px]" radius={"none"}>
        <CardBody className="overflow-hidden">
          <Tabs
            fullWidth
            aria-label="Tabs form"
            selectedKey={formSelected}
            size="md"
            onSelectionChange={setFormSelected}
          >
            <Tab key="login" title="Login" data-testid="login-tab">
              <form className="flex flex-col gap-4" onSubmit={handleLogin}>
                <Input
                  isRequired
                  label="Username"
                  placeholder="Enter your username"
                  type="username"
                  data-testid="login-username"
                  onChange={(e) => {setUsername(e.target.value)}}
                />
                <Input
                  isRequired
                  label="Password"
                  placeholder="Enter your password"
                  type="password"
                  data-testid="login-password"
                    onChange={(e) => {setPassword(e.target.value)}}
                />
                <p className="text-center text-small">
                  Need to create an account?{" "}
                  <Link size="sm" onPress={() => setFormSelected("sign-up")} data-testid="signup-link">
                    Sign up
                  </Link>
                </p>
                <div className="flex gap-2 justify-end">
                  <Button fullWidth color="primary" type="submit" data-testid="login-button">
                    Login
                  </Button>
                </div>
              </form>
            </Tab>
            <Tab key="sign-up" title="Sign up" data-testid="signup-tab">
              <form className="flex flex-col gap-4 h-[300px]" onSubmit={handleSignUp}>
                <Input
                  isRequired
                  label="Username"
                  placeholder="Enter your username"
                  type="username"
                  data-testid="signup-username"
                  onChange={(e) => {setUsername(e.target.value)}}
                />
                <Input
                  isRequired
                  label="Email"
                  placeholder="Enter your email"
                  type="email"
                  data-testid="signup-email"
                  onChange={(e) => {setEmail(e.target.value)}}
                />
                <Input
                  isRequired
                  label="Password"
                  placeholder="Enter your password"
                  type="password"
                  data-testid="signup-password"
                  onChange={(e) => {setPassword(e.target.value)}}
                />
                <p className="text-center text-small">
                  Already have an account?{" "}
                  <Link size="sm" onPress={() => setFormSelected("login")} data-testid="login-link">
                    Login
                  </Link>
                </p>
                <div className="flex gap-2 justify-end">
                  <Button fullWidth color="primary" type="submit" data-testid="signup-button">
                    Sign up
                  </Button>
                </div>
              </form>
            </Tab>
          </Tabs>
        </CardBody>
      </Card>
    </div>
  );
};
