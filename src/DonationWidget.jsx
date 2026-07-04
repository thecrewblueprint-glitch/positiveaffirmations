import './DonationWidget.css'

export default function DonationWidget() {
  const SPONSOR_LINK = 'https://github.com/sponsors/thecrewblueprint-glitch'

  return (
    <a href={SPONSOR_LINK} target="_blank" rel="noopener noreferrer" className="donation-button">
      💝 Support Development
    </a>
  )
}
