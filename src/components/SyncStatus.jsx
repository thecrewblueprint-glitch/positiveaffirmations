import './SyncStatus.css'

export default function SyncStatus({ success, message }) {
  return (
    <div className={`sync-status ${success ? 'success' : 'error'}`}>
      <span className="status-icon">
        {success ? '✓' : '✕'}
      </span>
      <span className="status-message">{message}</span>
    </div>
  )
}
