import { useState } from 'react'
import './CalendarPicker.css'

export default function CalendarPicker({ selectedDate, onDateSelect, affirmationCount }) {
  const [currentMonth, setCurrentMonth] = useState(new Date())

  const getDaysInMonth = (date) => new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate()
  const getFirstDayOfMonth = (date) => new Date(date.getFullYear(), date.getMonth(), 1).getDay()

  const prevMonth = () => setCurrentMonth(new Date(currentMonth.getFullYear(), currentMonth.getMonth() - 1))
  const nextMonth = () => setCurrentMonth(new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1))

  const days = []
  const daysInMonth = getDaysInMonth(currentMonth)
  const firstDay = getFirstDayOfMonth(currentMonth)

  for (let i = 0; i < firstDay; i++) {
    days.push(null)
  }
  for (let i = 1; i <= daysInMonth; i++) {
    days.push(new Date(currentMonth.getFullYear(), currentMonth.getMonth(), i))
  }

  const isSelected = (date) => {
    return date && date.toDateString() === selectedDate.toDateString()
  }

  const monthName = currentMonth.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })

  return (
    <div className="calendar-picker">
      <div className="calendar-header">
        <button onClick={prevMonth} className="nav-button">←</button>
        <h4>{monthName}</h4>
        <button onClick={nextMonth} className="nav-button">→</button>
      </div>

      <div className="calendar-weekdays">
        {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
          <div key={day} className="weekday">{day}</div>
        ))}
      </div>

      <div className="calendar-days">
        {days.map((date, idx) => (
          date ? (
            <button
              key={idx}
              className={`calendar-day ${isSelected(date) ? 'selected' : ''}`}
              onClick={() => onDateSelect(date)}
            >
              {date.getDate()}
            </button>
          ) : (
            <div key={idx} className="calendar-empty"></div>
          )
        ))}
      </div>

      <div className="calendar-legend">
        <p className="legend-text">
          <span>{affirmationCount}</span> affirmations available
        </p>
      </div>
    </div>
  )
}
