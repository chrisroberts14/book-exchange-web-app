import React from 'react';
import Login_Form from "./components/login_form/login_form";

const App = () => {
  const [username, setUsername] = React.useState('');
  const [password, setPassword] = React.useState('');

  return (
    <Login_Form username={username} setUsername={setUsername} password={password} setPassword={setPassword} />
  )
}

export default App;
