import * as axios from "axios";
import {login} from "./api_calls.js";

jest.mock('axios');

describe('login api call', () => {
    it('should return user data on success', async () => {
        axios.post.mockResolvedValue({data: {username: 'test', password: 'test'}});
        const data = await login({username: "test", password: "test"});
        expect(data).toStrictEqual({username: 'test', password: 'test'});
    });
    it('should return null on failure', async () => {
        axios.post.mockResolvedValue({data: null});
        const data = await login({username: "test", password: "test"});
        expect(data).toBe(null);
    });
});
