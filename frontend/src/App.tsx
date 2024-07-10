import { useState } from 'react';
import LoginForm from "./components/login_form/login_form";

const App = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [user, setUser] = useState(null);

  return (
    <LoginForm username={username} setUsername={setUsername} password={password} setPassword={setPassword} setUser={setUser} />
  )
}

export default App;
