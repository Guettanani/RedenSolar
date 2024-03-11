import React, { useEffect, useState } from 'react';

import 'bootstrap/dist/css/bootstrap.min.css';

const FiltreYear = ({ SelectedYear }) => {
    const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());

    const selectYear = (direction) => {
        const newYear = direction === 'next' ? selectedYear + 1 : selectedYear - 1;
        setSelectedYear(newYear);
    }

    useEffect(() => {
        SelectedYear(selectedYear);
    }, [selectedYear]);
    
    useEffect(() => {
        SelectedYear(selectedYear);
    }, []);

    return (
        <div id="year-selector" className='d-flex flex-column justify-content-center align-items-center'>
            <h3>Année</h3>
            <div id="div-buttons" className='d-flex flex-row justify-content-center align-items-center gap-2'>
                <button className='btn btn-outline-secondary' onClick={() => selectYear('prev')}>&lt;</button>
                <p className='display-6 m-0'>{selectedYear}</p>
                <button className='btn btn-outline-secondary' onClick={() => selectYear('next')}>&gt;</button>
            </div>
        </div>
    );
}


export default FiltreYear;
