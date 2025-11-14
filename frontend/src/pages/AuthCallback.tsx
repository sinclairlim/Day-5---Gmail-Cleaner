import { useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'

interface AuthCallbackProps {
  onSuccess: () => void
}

function AuthCallback({ onSuccess }: AuthCallbackProps) {
  const navigate = useNavigate()
  const location = useLocation()

  useEffect(() => {
    if (location.pathname === '/auth/success') {
      onSuccess()
      navigate('/dashboard')
    } else {
      alert('Authentication failed. Please try again.')
      navigate('/')
    }
  }, [location, navigate, onSuccess])

  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      height: '100vh',
      color: 'white',
      fontSize: '1.5rem'
    }}>
      Processing authentication...
    </div>
  )
}

export default AuthCallback
