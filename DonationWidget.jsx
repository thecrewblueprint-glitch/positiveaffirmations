/**
 * Minimal Donation Button Component
 * Drops into your dashboard footer or header
 *
 * Usage:
 *   import DonationButton from './DonationWidget'
 *   <DonationButton />
 */

import React from 'react'
import './DonationWidget.css'

export default function DonationButton() {
  const SPONSOR_LINK = 'https://github.com/sponsors/thecrewblueprint-glitch'

  return (
    <a href={SPONSOR_LINK} target="_blank" rel="noopener noreferrer" className="donation-button">
      💝 Support Development
    </a>
  )
}
