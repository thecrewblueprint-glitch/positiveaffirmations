import './Header.css'
import DonationWidget from '../DonationWidget'

export default function Header({ user, onLogout }) {
  return (
    <header className="header">
      <div className="header-container">
        <div className="header-left">
          <h1 className="logo">💝 Daily Affirmations</h1>
        </div>

        <div className="header-right">
          <DonationWidget />
          <div className="user-menu">
            <span className="user-name">{user?.email?.split('@')[0]}</span>
            <button className="btn-logout" onClick={onLogout}>
              Sign Out
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}
