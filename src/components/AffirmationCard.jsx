import { useState } from 'react'
import './AffirmationCard.css'

export default function AffirmationCard({ affirmation, onUpdate }) {
  const [isEditing, setIsEditing] = useState(false)
  const [text, setText] = useState(affirmation.text)

  const handleSave = () => {
    onUpdate(affirmation.id, text)
    setIsEditing(false)
  }

  const handleCancel = () => {
    setText(affirmation.text)
    setIsEditing(false)
  }

  return (
    <div className="affirmation-card">
      {isEditing ? (
        <div className="edit-mode">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="edit-textarea"
            rows="4"
          />
          <div className="edit-buttons">
            <button className="btn-save" onClick={handleSave}>
              ✓ Save
            </button>
            <button className="btn-cancel" onClick={handleCancel}>
              ✕ Cancel
            </button>
          </div>
        </div>
      ) : (
        <div className="view-mode">
          <p className="affirmation-text">{affirmation.text}</p>
          <div className="affirmation-meta">
            <span className="theme-badge">{affirmation.theme || 'General'}</span>
            <button
              className="btn-edit"
              onClick={() => setIsEditing(true)}
            >
              ✏️ Edit
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
