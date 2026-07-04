import { useState, useEffect } from 'react'
import './LoginPage.css'
import DonationWidget from '../DonationWidget'

const API_URL = 'https://affirmations-api.onrender.com'

export default function LoginPage() {
  const [authUrl, setAuthUrl] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchAuthUrl()
  }, [])

  const fetchAuthUrl = async () => {
    try {
      const response = await fetch(`${API_URL}/auth/google/start`)
      if (!response.ok) throw new Error('Failed to get auth URL')
      const data = await response.json()
      setAuthUrl(data.auth_url)
    } catch (err) {
      setError('Failed to load login. Please try again.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-content">
          <h1>Daily Affirmations</h1>
          <p className="tagline">365 days of positive affirmations synced to your calendar</p>

          <div className="login-box">
            <h2>Get Started</h2>
            <p>Sign in with Google to generate your personalized affirmations</p>

            {loading ? (
              <button className="btn-primary" disabled>
                Loading...
              </button>
            ) : error ? (
              <div className="error-message">{error}</div>
            ) : (
              <a href={authUrl} className="btn-primary">
                Sign in with Google
              </a>
            )}

            <div className="features">
              <div className="feature">
                <span className="feature-icon">✨</span>
                <span>365 unique affirmations</span>
              </div>
              <div className="feature">
                <span className="feature-icon">📅</span>
                <span>Synced to Google Calendar</span>
              </div>
              <div className="feature">
                <span className="feature-icon">✏️</span>
                <span>Customize your affirmations</span>
              </div>
            </div>
          </div>
        </div>

        <footer className="login-footer">
          <DonationWidget />
          <p>Built with 💝 to inspire daily growth</p>
        </footer>
      </div>
    </div>
  )
}
