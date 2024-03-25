import React, { useEffect, useState } from 'react';
import Calendar2 from './Calendar2';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../../App.css';

const FiltreDate = ({ onDateRangeSelect, UnselectDate, OnDateMode }) => {
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [selectedPeriod, setSelectedPeriod] = useState(OnDateMode ? 'none' : '1 semaine');
  const [ShowCalendar, setShowCalendar] = useState(false);

  const handleDateSelect = (date) => {
    // console.log(date);
    if (date && date.length === 2) {
      const FinalDate = [];
      date.forEach(adate => {
        const newDate = new Date(adate);
        // newDate.setDate(adate.getDate());
        FinalDate.push(newDate);
        // console.log(adate);
      });
      setStartDate(FinalDate[0].toISOString().split('T')[0]);
      setEndDate(FinalDate[1].toISOString().split('T')[0]);
      // console.log(startDate);
      // console.log(endDate);
    }
  };

  const handleEndDateSelect = (date) => {
    if (date) {
      setEndDate(date.toISOString().split('T')[0]);
    }
  };
  const handleStartDateSelect = (date) => {
    if (date) {
      setEndDate(date.toISOString().split('T')[0]);
    }
  };
  const handlePeriodChange = (e) => {
    const selectedValue = e.target.value;
    let RangeDate = new Date(); // Initialiser avec la date actuelle
    let today = new Date(); // Initialiser avec la date actuelle
    let showCalendar = false;

    if (selectedValue === '1 semaine') {
      RangeDate.setDate(RangeDate.getDate() - 7);
      setStartDate(RangeDate.toISOString().split('T')[0]);
      setEndDate(today.toISOString().split('T')[0]);
      // Mettre à jour showCalendar ici si nécessaire
    } else if (selectedValue === '2 semaines') {
      RangeDate.setDate(RangeDate.getDate() - 14);
      setStartDate(RangeDate.toISOString().split('T')[0]);
      setEndDate(today.toISOString().split('T')[0]);
      // Mettre à jour showCalendar ici si nécessaire
    } else if (selectedValue === '1 mois') {
      RangeDate.setDate(1);
      setStartDate(RangeDate.toISOString().split('T')[0]);
      setEndDate(today.toISOString().split('T')[0]);
      // Mettre à jour showCalendar ici si nécessaire
    } else if (selectedValue === 'Autre') {
      // Définir showCalendar sur true si la valeur est 'Autre'
      showCalendar = true;
    }

    // Mettre à jour l'état showCalendar en fonction de la logique ci-dessus
    setShowCalendar(showCalendar);

    // Mettre à jour l'état selectedPeriod avec la valeur sélectionnée
    setSelectedPeriod(selectedValue);
  };

  useEffect(() => {
    onDateRangeSelect(startDate, endDate);
    OnDateMode(selectedPeriod);
  }, [startDate, endDate, selectedPeriod]);

  useEffect(() => {
    InitPeriode();
  }, []);

  const InitPeriode = () => {
    setSelectedPeriod("1 semaine");
    const today = new Date();
    const oneWeekAgo = new Date(today);
    oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
    setStartDate(oneWeekAgo.toISOString().split('T')[0]);
    setEndDate(today.toISOString().split('T')[0]);
  }

  const close_calendar = () => {
    setShowCalendar(false);
    if (selectedPeriod === 'autre' && (!startDate || !endDate)) {
      setSelectedPeriod("1 semaine");
      const today = new Date();
      const oneWeekAgo = new Date(today);
      oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
      setStartDate(oneWeekAgo.toISOString().split('T')[0]);
      setEndDate(today.toISOString().split('T')[0]);
    }
  }

  return (
    <div className="col-lg-3 col-4 position-relative ">

      <label htmlFor="periodSelect" className="form-label text-light">Période:</label>
      <select id="periodSelect" className="form-select" value={selectedPeriod} onClick={(e) => handlePeriodChange(e)} onChange={(e) => handlePeriodChange(e)}>
        {UnselectDate ? <option value="none">none</option> : null}
        <option value="1 semaine">1 semaine</option>
        <option value="2 semaines">2 semaines</option>
        <option value="1 mois">1 mois</option>
        <option value="Autre">Autre</option>
      </select>

      <div className="d-flex gap-2 flex-row justify-content-around text-light m-1">
        <label className="border m-1 p-2 rounded">Début : {startDate || ''}</label>
        <label className="border m-1 p-2 rounded">Fin : {endDate || ''}</label>
      </div>

      <div id="calendar-overlay" className={`position-absolute top-100 start-0 bg-secondary rounded p-2 m-1 z-index-999 ${ShowCalendar ? '' : 'd-none'}`}>
        <div id="frame" className='container-fluid d-flex flex-column justify-content-center align-items-center'>
          <button className='btn btn-danger ms-auto' onClick={close_calendar}>X</button>
          <div className='col-12 d-flex flex-row align-items-center justify-content-center p-1 gap-1'>
            <label htmlFor='CalendarStartDate' className='form-label col-4'>Date de début: </label>
            <input
              id="CalendarStartDate"
              className='form-control-sm col-8'
              style={{ maxHeight: "30px" }}
              type="date"
              value={startDate || ''}
              onChange={(e) => handleStartDateSelect(new Date(e.target.value))}
            />
          </div>
          <div className='col-12 d-flex flex-row align-items-center justify-content-center p-1 gap-1'>
            <label htmlFor='CalendarEndDate' className='form-label col-4'>Date de fin: </label>
            <input
              id="CalendarEndDate"
              className='form-control-sm col-8'
              style={{ maxHeight: "30px" }}
              type="date"
              value={endDate || ''}
              onChange={(e) => handleEndDateSelect(new Date(e.target.value))}
            />
          </div>
          <div>
            <Calendar2 onDateRangeSelect={handleDateSelect} />
          </div>
          <button className='btn btn-success mt-2 col-6' onClick={() => setShowCalendar(false)}>Valider</button>
        </div>
      </div>
    </div>
  );
};

export default FiltreDate;