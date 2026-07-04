import { useState, useEffect } from 'react'
import './DashboardPage.css'
import AffirmationCard from '../components/AffirmationCard'
import CalendarPicker from '../components/CalendarPicker'
import SyncStatus from '../components/SyncStatus'

export default function DashboardPage({ user }) {
  const [affirmations, setAffirmations] = useState([])
  const [selectedDate, setSelectedDate] = useState(new Date())
  const [currentAffirmation, setCurrentAffirmation] = useState(null)
  const [loading, setLoading] = useState(true)
  const [syncing, setSyncing] = useState(false)
  const [syncStatus, setSyncStatus] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadAffirmations()
  }, [user])

  useEffect(() => {
    const affirmation = affirmations.find(a =>
      new Date(a.affirmation_date).toDateString() === selectedDate.toDateString()
    )
    setCurrentAffirmation(affirmation)
  }, [selectedDate, affirmations])

  const loadAffirmations = async () => {
    try {
      setLoading(true)
      const response = await fetch('http://localhost:8000/affirmations/', {
        headers: { 'X-User-ID': user.id }
      })
      if (!response.ok) throw new Error('Failed to load affirmations')
      const data = await response.json()
      setAffirmations(data)
    } catch (err) {
      setError('Failed to load affirmations')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleSync = async () => {
    try {
      setSyncing(true)
      const response = await fetch('http://localhost:8000/calendar/sync', {
        method: 'POST',
        headers: { 'X-User-ID': user.id }
      })
      if (!response.ok) throw new Error('Sync failed')
      setSyncStatus({ success: true, message: 'Affirmations synced to Google Calendar!' })
      loadAffirmations()
      setTimeout(() => setSyncStatus(null), 3000)
    } catch (err) {
      setSyncStatus({ success: false, message: 'Sync failed. Please try again.' })
      console.error(err)
    } finally {
      setSyncing(false)
    }
  }

  const handleUpdateAffirmation = async (id, text) => {
    try {
      const response = await fetch(`http://localhost:8000/affirmations/${id}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'X-User-ID': user.id
        },
        body: JSON.stringify({ text })
      })
      if (!response.ok) throw new Error('Update failed')
      loadAffirmations()
    } catch (err) {
      console.error(err)
    }
  }

  if (loading) {
    return <div className="loading-spinner"></div>
  }

  return (
    <div className="dashboard">
      <div className="dashboard-container">
        <aside className="sidebar">
          <div className="sidebar-section">
            <h3>Calendar</h3>
            <CalendarPicker
              selectedDate={selectedDate}
              onDateSelect={setSelectedDate}
              affirmationCount={affirmations.length}
            />
          </div>

          <div className="sidebar-section">
            <button
              className="btn-sync"
              onClick={handleSync}
              disabled={syncing}
            >
              {syncing ? '⏳ Syncing...' : '📅 Sync to Calendar'}
            </button>
          </div>

          {syncStatus && (
            <SyncStatus
              success={syncStatus.success}
              message={syncStatus.message}
            />
          )}

          <div className="sidebar-stats">
            <div className="stat">
              <span className="stat-value">{affirmations.length}</span>
              <span className="stat-label">Affirmations</span>
            </div>
          </div>
        </aside>

        <main className="main-content">
          {error && (
            <div className="error-banner">{error}</div>
          )}

          {currentAffirmation ? (
            <div className="affirmation-section">
              <div className="date-display">
                {selectedDate.toLocaleDateString('en-US', {
                  weekday: 'long',
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric'
                })}
              </div>
              <AffirmationCard
                affirmation={currentAffirmation}
                onUpdate={handleUpdateAffirmation}
              />
            </div>
          ) : (
            <div className="empty-state">
              <p>No affirmation for this date yet.</p>
              <button className="btn-sync" onClick={handleSync}>
                Generate Affirmations
              </button>
            </div>
          )}

          <div className="all-affirmations">
            <h3>All Affirmations</h3>
            <div className="affirmations-grid">
              {affirmations.slice(0, 10).map(aff => (
                <div key={aff.id} className="affirmation-preview">
                  <div className="preview-date">
                    {new Date(aff.affirmation_date).toLocaleDateString()}
                  </div>
                  <p>{aff.text}</p>
                </div>
              ))}
            </div>
            {affirmations.length > 10 && (
              <p className="more-count">+ {affirmations.length - 10} more affirmations</p>
            )}
          </div>
        </main>
      </div>
    </div>
  )
}
