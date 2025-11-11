import { useState } from 'react'
import api from '../api/axios'

function AuthForm() {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleLogin = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setSuccess(false)

    try {
      const params = new URLSearchParams()
      params.append('username', formData.username)
      params.append('password', formData.password)

      const response = await api.post('/login', params, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      })
      
      setSuccess(true)
      localStorage.setItem('token', response.data.session_token || 'demo-token')
      
      setTimeout(() => {
        setSuccess(false)
      }, 3000)
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = async () => {
    try {
      await api.post('/logout')
      localStorage.removeItem('token')
      setSuccess(true)
      setFormData({ username: '', password: '' })
    } catch (err) {
      setError('Logout failed')
    }
  }

  const isLoggedIn = !!localStorage.getItem('token')

  if (isLoggedIn) {
    return (
      <div className="card">
        <h2 className="card-header">You're Logged In</h2>
        {success && <div className="alert alert-success">Logged out successfully!</div>}
        <p>You are currently authenticated.</p>
        <button className="btn btn-danger" onClick={handleLogout}>
          Logout
        </button>
      </div>
    )
  }

  return (
    <div className="card">
      <h2 className="card-header">Login</h2>
      
      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">Login successful!</div>}

      <form onSubmit={handleLogin}>
        <div className="form-group">
          <label>Username</label>
          <input
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
            placeholder="admin"
          />
        </div>

        <div className="form-group">
          <label>Password</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            placeholder="secret"
          />
        </div>

        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>

      <p style={{ marginTop: '1rem', fontSize: '0.9rem', opacity: 0.7 }}>
        Try username: <code>admin</code> / password: <code>secret</code>
      </p>
    </div>
  )
}

export default AuthForm