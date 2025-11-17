import { useState } from 'react'
import { login } from '../services/api'
import { Mail, Sparkles } from 'lucide-react'
import './LoginPage.css'

function LoginPage() {
  const [loading, setLoading] = useState(false)

  const handleLogin = async () => {
    setLoading(true)
    try {
      const { auth_url } = await login()
      window.location.href = auth_url
    } catch (error) {
      console.error('Login failed:', error)
      alert('Login failed. Please try again.')
      setLoading(false)
    }
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <Mail size={48} className="logo-icon" />
          <h1>Gmail Cleaner</h1>
          <p className="subtitle">AI-Powered Email Management</p>
        </div>

        <div className="features">
          <div className="feature">
            <Sparkles size={24} />
            <span>Smart spam detection</span>
          </div>
          <div className="feature">
            <Sparkles size={24} />
            <span>Find large emails</span>
          </div>
          <div className="feature">
            <Sparkles size={24} />
            <span>Clean old messages</span>
          </div>
        </div>

        <button
          className="login-button"
          onClick={handleLogin}
          disabled={loading}
        >
          {loading ? 'Connecting...' : 'Sign in with Google'}
        </button>

        <p className="disclaimer">
          We only request read and modify permissions for your Gmail.
          Your emails are never stored on our servers.
        </p>
      </div>
    </div>
  )
}

export default LoginPage
