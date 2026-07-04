import { useState, useEffect } from 'react'
import './App.css'
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import Header from './components/Header'
import { getToken, setToken, clearToken, authFetch } from './api'

export default function App() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    init()
  }, [])

  const init = async () => {
    try {
      // The OAuth callback redirects back here with the token in the URL
      // fragment: #token=<jwt>.
      const hash = window.location.hash.startsWith('#')
        ? window.location.hash.slice(1)
        : window.location.hash
      const urlToken = new URLSearchParams(hash).get('token')
      if (urlToken) {
        setToken(urlToken)
        window.history.replaceState({}, document.title, '/')
      }

      if (getToken()) {
        const res = await authFetch('/auth/me')
        if (res.ok) {
          setUser(await res.json())
        } else {
          clearToken()
        }
      }
    } catch (error) {
      console.error('Auth init failed:', error)
      clearToken()
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    clearToken()
    setUser(null)
  }

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="loading-spinner"></div>
        <p>Loading affirmations...</p>
      </div>
    )
  }

  if (!user) {
    return <LoginPage />
  }

  return (
    <div className="app">
      <Header user={user} onLogout={handleLogout} />
      <DashboardPage user={user} />
    </div>
  )
}
