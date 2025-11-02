import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import loginPic from '../assets/login_pic.jpg'
import bmwLogo from '../assets/rybmw.jpg'

function Register() {
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    if (password !== confirmPassword) {
      setError('Hasła nie są takie same')
      return
    }

    setIsLoading(true)

    try {
      const response = await fetch('http://localhost:8000/register', {
        method: 'POST',
        headers: {
          'accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          "username": username,
          "email": email,
          "password": password
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Błąd rejestracji')
      }

      // Registration successful - redirect to login
      navigate('/login')
    } catch (err) {
      setError(err.message || 'Wystąpił błąd podczas rejestracji')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="login-container">
      <div className="login-image" aria-hidden>
        <img
          src={loginPic}
          alt="Ilustracja rejestracji"
        />
      </div>
      <div className="login-layout">
        <form onSubmit={handleSubmit} className="login-form">
          <div className="logo-container">
            <img src={bmwLogo} alt="BMW Logo" className="bmw-logo" />
          </div>
          {error && <div className="error-message">{error}</div>}
          <div className="form-group">
            <label htmlFor="username">Nazwa użytkownika:</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              disabled={isLoading}
            />
          </div>
          <div className="form-group">
          <label htmlFor="email">Email</label>
            <input
              type="text"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={isLoading}
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Hasło:</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={isLoading}
            />
          </div>
          <div className="form-group">
            <label htmlFor="confirmPassword">Potwierdź hasło:</label>
            <input
              type="password"
              id="confirmPassword"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              disabled={isLoading}
            />
          </div>
          <button type="submit" disabled={isLoading}>
            {isLoading ? 'Rejestracja...' : 'Zarejestruj się'}
          </button>
          <p className="form-footer">
            Masz już konto? <Link to="/login">Zaloguj się</Link>
          </p>
        </form>
      </div>
    </div>
  )
}

export default Register