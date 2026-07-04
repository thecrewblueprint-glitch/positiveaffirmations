/**
 * Donation Widget Component
 * Use in your React app:
 *   import DonationWidget from './DonationWidget'
 *   <DonationWidget />
 */

import React, { useState } from 'react'
import './DonationWidget.css'

export default function DonationWidget() {
  const [customAmount, setCustomAmount] = useState('')
  const [showThankYou, setShowThankYou] = useState(false)

  const PAYPAL_EMAIL = 'your-paypal-email@example.com' // TODO: Replace with your PayPal email

  const donate = (amount) => {
    const paypalUrl = `https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=${PAYPAL_EMAIL}&item_name=Daily+Affirmations+Donation&amount=${amount}&currency_code=USD&return=${window.location.origin}/thank-you`

    // Log donation on backend (optional)
    fetch('/api/donations/log', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        amount,
        payment_platform: 'paypal',
        message: `Donated $${amount}`,
      }),
    }).catch(err => console.log('Donation logged'))

    // Redirect to PayPal
    window.location.href = paypalUrl
  }

  const donateCustom = () => {
    const amount = parseFloat(customAmount)
    if (!amount || amount < 1 || amount > 10000) {
      alert('Please enter a valid amount ($1-$10,000)')
      return
    }
    donate(amount)
  }

  return (
    <div className="donation-widget">
      <div className="donation-card">
        <h2>
          Support This Project <span className="heart">❤️</span>
        </h2>
        <p className="subtitle">
          Help keep Daily Affirmations free and growing. Your support means everything.
        </p>

        <div className="buttons-grid">
          <button className="donation-btn" onClick={() => donate(1)}>
            ☕ $1
          </button>
          <button className="donation-btn" onClick={() => donate(2)}>
            🌟 $2
          </button>
          <button className="donation-btn" onClick={() => donate(5)}>
            💝 $5
          </button>
          <button className="donation-btn" onClick={() => donate(10)}>
            ✨ $10
          </button>
        </div>

        <div className="custom-section">
          <label className="custom-label">Custom Amount (USD)</label>
          <div className="custom-input-wrapper">
            <span className="dollar-sign">$</span>
            <input
              type="number"
              className="custom-input"
              placeholder="Enter amount"
              min="1"
              max="10000"
              value={customAmount}
              onChange={(e) => setCustomAmount(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && donateCustom()}
            />
          </div>
          <button className="custom-btn" onClick={donateCustom}>
            Donate Custom Amount
          </button>
        </div>

        <div className="note">
          <strong>🔒 Secure:</strong> Donations are processed through PayPal. We never store your payment info.
        </div>
      </div>
    </div>
  )
}
