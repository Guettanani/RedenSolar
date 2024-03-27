import React, { useEffect, useState } from 'react';
import Calendar2 from './Calendar2';

const FiltreDate = ({ onDateRangeSelect, UnselectDate, OnDateMode }) => {
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [selectedPeriod, setSelectedPeriod] = useState(OnDateMode ? 'none' : 'Mois en cours');
  const [ShowCalendar, setShowCalendar] = useState(false);
  const [CalendarContent, setCalendarContent] = useState(false);

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
      setCalendarContent(true);
      setSelectedPeriod('Personalisé');
      setStartDate(FinalDate[0].toISOString().split('T')[0]);
      setEndDate(FinalDate[1].toISOString().split('T')[0]);
      // console.log(startDate);
      // console.log(endDate);
    }
  };

  // const handleEndDateSelect = (date) => {
  //   if (date) {
  //     setEndDate(date.toISOString().split('T')[0]);
  //   }
  // };
  // const handleStartDateSelect = (date) => {
  //   if (date) {
  //     setEndDate(date.toISOString().split('T')[0]);
  //   }
  // };
  const handlePeriodChange = (e) => {
    const selectedValue = e.target.innerText;
    ChangeDatePeriode(selectedValue);
    setSelectedPeriod(selectedValue);
  };

  const ChangeDatePeriode = (SelectedPeriode) => {
    if (SelectedPeriode === 'Personalisé') {
      console.log('Personalisé');
    }
    else if (SelectedPeriode === 'Mois en cours') {
      const today = new Date();
      const oneMonthAgo = new Date(today);
      oneMonthAgo.setDate(1);
      console.log("end : " + today);
      console.log("start : " + oneMonthAgo);
      setEndDate(today.toISOString().split('T')[0]);
      setStartDate(oneMonthAgo.toISOString().split('T')[0]);
      setCalendarContent(false);
    }
    else if (SelectedPeriode === 'Mois dernier') {
      const today = new Date();
      const oneMonthAgo = new Date(today);
      oneMonthAgo.setMonth(oneMonthAgo.getMonth() - 1);
      oneMonthAgo.setDate(1);
      const endDate = new Date(today.getFullYear(), today.getMonth(), 0); // Définit la date sur le dernier jour du mois précédent
      console.log("end : " + endDate);
      console.log("start : " + oneMonthAgo);
      setEndDate(endDate.toISOString().split('T')[0]);
      setStartDate(oneMonthAgo.toISOString().split('T')[0]);
      setCalendarContent(false);
    }
    else if (SelectedPeriode === 'None') {
      setStartDate(null);
      setEndDate(null);
      setCalendarContent(false);
    }
  }

  useEffect(() => {
    onDateRangeSelect(startDate, endDate);
    // OnDateMode(selectedPeriod);
  }, [startDate, endDate, selectedPeriod]);

  useEffect(() => {
    if (!UnselectDate) {
      console.log(selectedPeriod);
      ChangeDatePeriode(selectedPeriod);
    }
  }, []);

  const close_calendar = () => {
    setShowCalendar(false);
    if (selectedPeriod === 'Personalisé' && (!startDate || !endDate)) {
      setSelectedPeriod("Mois en cours");
    }
  }

  return (
    <div className="col-lg-3 col-4 position-relative">
      <div className='col-12 d-flex flex-row justify-content-center align-items-center m-1'>
        <button className="btn btn-secondary" onClick={() => setShowCalendar(true)}>
          Afficher le calendrier
        </button>
      </div>


      <div className="d-flex gap-2 flex-row justify-content-around text-light m-1 mt-2">
        <label className="border m-1 p-1 rounded">Début : {startDate || ''}</label>
        <label className="border m-1 p-1 rounded">Fin : {endDate || ''}</label>
      </div>

      {ShowCalendar
        &&
        <div id="calendar-overlay" className="position-absolute top-100 end-0 bg-light rounded z-index-999 d-flex flex-column align-items-center justify-content-center">
          <div id="frame" className='container-fluid p-0 position-relative d-flex flex-row justify-content-center align-items-start'>
            {/* Bouton de fermeture du calendrier */}
            <button className='position-absolute top-0 end-0 btn btn-outline-danger m-1' onClick={close_calendar}>X</button>

            {/* Liste sous forme de sidebar à gauche */}
            <div className='col-4 mt-5 d-flex flex-column align-items-center justify-content-center'>
              <div className="col-8 text-center d-flex flex-column justify-content-center align-items-center gap-3 p-0 mx-3">
                {
                  OnDateMode &&
                  <button onClick={handlePeriodChange} className={`btn btn-outline-info text-dark rounded border-primary-subtle ${selectedPeriod === 'none' ? "bg-info bg-opacity-25" : ""}`} disabled={selectedPeriod === 'none'}>None</button>
                }
                <button onClick={handlePeriodChange} className={`btn btn-outline-info text-dark rounded border-primary-subtle ${selectedPeriod === 'Mois en cours' ? "bg-info bg-opacity-25" : ""}`}>Mois en cours</button>
                <button onClick={handlePeriodChange} className={`btn btn-outline-info text-dark rounded border-primary-subtle ${selectedPeriod === 'Mois dernier' ? "bg-info bg-opacity-25" : ""}`}>Mois dernier</button>
                <button onClick={handlePeriodChange} className={`btn btn-outline-info text-dark rounded border-primary-subtle ${selectedPeriod === 'Personalisé' ? "bg-info bg-opacity-25" : ""}`}>Personnalisé</button>
              </div>
            </div>


            {/* Calendrier à droite */}
            <div className='col mt-5 me-3'>
              <div>
                <Calendar2 onDateRangeSelect={handleDateSelect} CalendarContent={CalendarContent} />
              </div>
            </div>
          </div>
          <button className='btn btn-success m-2 col-10' onClick={() => setShowCalendar(false)}>Valider</button>

        </div>

      }
    </div>
  );
};

export default FiltreDate;