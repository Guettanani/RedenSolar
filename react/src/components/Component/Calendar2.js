import React, { useState } from 'react';
import './Calendar.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const Calendar2 = ({ onDateRangeSelect }) => {
    const [startDate, setStartDate] = useState(null);
    const [endDate, setEndDate] = useState(null);
    const [currentDate, setCurrentDate] = useState(new Date());

    const handleDateClick = (date) => {
        if (!startDate) {
            setStartDate(date);
        } else if (!endDate && date > startDate) {
            setEndDate(date);
            if (onDateRangeSelect) {
                onDateRangeSelect([startDate, date]);
            }
        } else {
            setStartDate(date);
            setEndDate(null);
        }
    };

    const handlePrevMonth = () => {
        setCurrentDate(prevDate => {
            const prevMonthDate = new Date(prevDate);
            prevMonthDate.setMonth(prevDate.getMonth() - 1);
            return prevMonthDate;
        });
    };

    const handleNextMonth = () => {
        setCurrentDate(prevDate => {
            const nextMonthDate = new Date(prevDate);
            nextMonthDate.setMonth(prevDate.getMonth() + 1);
            return nextMonthDate;
        });
    };

    const renderCalendarDays = () => {
        const days = [];
        const currentMonth = currentDate.getMonth();
        const year = currentDate.getFullYear();
        const firstDayOfMonth = new Date(year, currentMonth, 1);
        const lastDayOfMonth = new Date(year, currentMonth + 1, 0);
        const daysInMonth = lastDayOfMonth.getDate();

        // Ajouter les jours du mois
        for (let i = 1; i <= daysInMonth; i++) {
            const currentDate = new Date(year, currentMonth, i);
            days.push({
                date: currentDate,
                day: i,
                isStart: startDate && currentDate.getTime() === startDate.getTime(),
                isEnd: endDate && currentDate.getTime() === endDate.getTime(),
                isSelected: startDate && endDate && currentDate > startDate && currentDate < endDate,
            });
        }

        // Ajouter les jours du mois précédent nécessaires pour compléter la semaine
        for (let i = 0; i < firstDayOfMonth.getDay(); i++) {
            const previousMonthDay = new Date(year, currentMonth, -i);
            days.unshift({ date: previousMonthDay, day: previousMonthDay.getDate(), isOutside: true });
        }

        // Ajouter les jours du mois suivant nécessaires pour compléter la semaine
        const lastDayOfWeek = new Date(lastDayOfMonth);
        lastDayOfWeek.setDate(lastDayOfMonth.getDate() + (6 - lastDayOfMonth.getDay()));
        for (let i = 1; i <= 6 - lastDayOfMonth.getDay(); i++) {
            const nextMonthDay = new Date(lastDayOfMonth.getFullYear(), lastDayOfMonth.getMonth() + 1, i);
            days.push({ date: nextMonthDay, day: nextMonthDay.getDate(), isOutside: true });
        }

        return days.map((day, index) => (
            <div
                key={index}
                className={`calendar-day ${day.isStart ? 'start-date' : ''} ${day.isEnd ? 'end-date' : ''} ${day.isSelected ? 'selected-date' : ''} ${day.isOutside ? 'outside-month' : ''}`}
                onClick={() => handleDateClick(day.date)}
            >
                {day.day}
            </div>
        ));
    };

    return (
        <div className="calendar-container">
            <div className="calendar-header d-flex flex-column gap-1 justify-content-center align-items-center">
                <span className="month-year">{currentDate.toLocaleString('default', { month: 'long', year: 'numeric' })}</span>
                <div className='btn-group col-6'>
                    <button onClick={handlePrevMonth} className='btn btn-outline-secondary'>&lt;</button>
                    <button onClick={handleNextMonth} className='btn btn-outline-secondary'>&gt;</button>
                </div>
            </div>
            <div className="calendar-days">
                {renderCalendarDays()}
            </div>
        </div>
    );
};

export default Calendar2;
