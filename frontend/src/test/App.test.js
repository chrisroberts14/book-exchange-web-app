import { render, screen } from '@testing-library/react'
import App from '../App'

describe('App', () => {
    it('renders App component',
    () => {
        render(<App />)
        const linkElement = screen.getByText(/login/i)
        expect(linkElement).toBeInTheDocument()
    },
    )
})
