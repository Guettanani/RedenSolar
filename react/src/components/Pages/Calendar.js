import React, { useState } from 'react';
// import './Calendar.css';

const Calendar = ({ onSelectDate }) => {
  const [selectedDate, setSelectedDate] = useState(null);

  const daysInMonth = (year, month) => new Date(year, month + 1, 0).getDate();
  const getFirstDayOfMonth = (year, month) => new Date(year, month, 1).getDay();

  const getCurrentMonthDays = () => {
    const currentMonthDays = [];
    const totalDays = daysInMonth(
      selectedDate ? selectedDate.getFullYear() : new Date().getFullYear(),
      selectedDate ? selectedDate.getMonth() : new Date().getMonth()
    );
    const firstDayOfMonth = getFirstDayOfMonth(
      selectedDate ? selectedDate.getFullYear() : new Date().getFullYear(),
      selectedDate ? selectedDate.getMonth() : new Date().getMonth()
    );

    // Ajouter des jours vides pour atteindre le premier jour du mois
    for (let i = 0; i < firstDayOfMonth; i++) {
      currentMonthDays.push(null);
    }

    // Ajouter les jours du mois
    for (let i = 1; i <= totalDays; i++) {
      currentMonthDays.push(i);
    }

    return currentMonthDays;
  };

  const handleDateClick = (day) => {
    setSelectedDate(
      selectedDate
        ? new Date(selectedDate.getFullYear(), selectedDate.getMonth(), day)
        : new Date(new Date().getFullYear(), new Date().getMonth(), day)
    );

    if (onSelectDate) {
      onSelectDate(day);
      console.log('Date clicked in Calendar:', day);
    }
  };

  const renderDaysOfWeek = () => {
    const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    return daysOfWeek.map((day) => <div key={day} className="day-of-week">{day}</div>);
  };

  const renderCalendarDays = () => {
    const currentMonthDays = getCurrentMonthDays();
    return currentMonthDays.map((day, index) => (
      <div
        key={index}
        className={`calendar-day ${day !== null ? 'active' : 'inactive'} ${
          selectedDate && day === selectedDate.getDate() ? 'selected' : ''
        }`}
        onClick={() => (day !== null ? handleDateClick(day) : null)}
      >
        {day !== null ? day : ''}
      </div>
    ));
  };

};

export default Calendar;