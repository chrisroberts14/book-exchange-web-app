import {useState} from "react";
import {LoginForm} from './components/LoginForm/LoginForm';

export function App() {
    const [user, setUser] = useState(null);

    return (
        <div>
            <LoginForm user={user} setUser={setUser} />
        </div>
    )
}
