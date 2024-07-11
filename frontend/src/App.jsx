import {useState} from "react";
import {LoginForm} from './components/LoginForm/LoginForm';

export function App() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [user, setUser] = useState(null);

    return (
        <div>
            <LoginForm username={username} setUsername={setUsername} password={password} setPassword={setPassword} user={user} setUser={setUser} />
        </div>
    )
}
