import React, { useEffect, useState } from 'react';
import axios from 'axios';

// import './main_courante.css';
import 'bootstrap/dist/css/bootstrap.min.css';

import FiltreDate from '../Component/DateFiltre';
import FiltreCentrale from '../Component/CentraleFiltre';
import TableMainCourante from '../Component/MainCouranteTable';


export default function TstTab() {
    const today = new Date();
    const oneWeekAgo = new Date(today);
    const [selectionCentrale, setSelectionCentrale] = useState('Toutes');
    const [startDate, setStartDate] = useState(oneWeekAgo.toISOString().split('T')[0]);
    const [endDate, setEndDate] = useState(today.toISOString().split('T')[0]);
    const [DateMode, setDateMode] = useState('none');


    const handleDateSelect = (start, end) => {
        setStartDate(start);
        setEndDate(end);
    };

    return (
        <div className='container-fluid text-dark d-flex p-3 flex-column'>
            <div className='d-flex flex-wrap justify-content-around align-items-center gap-2 p-3 bg-dark rounded'>
                <FiltreCentrale setSelectionCentrale={setSelectionCentrale} AllowAll={true}/>
                <FiltreDate onDateRangeSelect={handleDateSelect} UnselectDate={true} OnDateMode={setDateMode}/>
            </div>
            <TableMainCourante startDate={startDate} endDate={endDate} SelectedCentrale={selectionCentrale} DateMode={DateMode}/>
        </div>
    );
}
