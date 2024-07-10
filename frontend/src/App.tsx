import React from 'react';
import LoginForm from "./components/login_form/login_form";

const App = () => {
  const [username, setUsername] = React.useState('');
  const [password, setPassword] = React.useState('');

  return (
    <LoginForm username={username} setUsername={setUsername} password={password} setPassword={setPassword} />
  )
}

export default App;
