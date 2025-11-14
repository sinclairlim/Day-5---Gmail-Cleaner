import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import AuthCallback from './pages/AuthCallback'
import { checkAuthStatus } from './services/api'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null)

  useEffect(() => {
    checkAuth()
  }, [])

  const checkAuth = async () => {
    try {
      const { authenticated } = await checkAuthStatus()
      setIsAuthenticated(authenticated)
    } catch (error) {
      setIsAuthenticated(false)
    }
  }

  if (isAuthenticated === null) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        color: 'white',
        fontSize: '1.5rem'
      }}>
        Loading...
      </div>
    )
  }

  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={isAuthenticated ? <Navigate to="/dashboard" /> : <LoginPage onLogin={() => setIsAuthenticated(true)} />}
        />
        <Route
          path="/dashboard"
          element={isAuthenticated ? <DashboardPage onLogout={() => setIsAuthenticated(false)} /> : <Navigate to="/" />}
        />
        <Route
          path="/auth/success"
          element={<AuthCallback onSuccess={() => setIsAuthenticated(true)} />}
        />
        <Route
          path="/auth/error"
          element={<AuthCallback onSuccess={() => setIsAuthenticated(false)} />}
        />
      </Routes>
    </Router>
  )
}

export default App
