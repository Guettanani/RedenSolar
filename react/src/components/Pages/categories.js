import { React, useState } from 'react';
// import axios from 'axios';

import FiltreDate from '../Component/DateFiltre';
import FiltreCentrale from '../Component/CentraleFiltre';
import FiltreSeuil from '../Component/SeuilFiltre';
import Tableau from '../Component/CategorisationTable';
import CategorisationModal from '../Component/ModalCategorisation';

import 'bootstrap/dist/css/bootstrap.min.css';



export default function Categories() {

  const today = new Date();
  const oneWeekAgo = new Date(today);
  oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
  const [selectionCentrale, setSelectionCentrale] = useState(null);
  const [startDate, setStartDate] = useState(oneWeekAgo.toISOString().split('T')[0]);
  const [endDate, setEndDate] = useState(today.toISOString().split('T')[0]);
  const [SeuilValeur, setSeuilValeur] = useState(null);
  const [ClickedData, setClickedData] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [onlyError, setOnlyError] = useState(false);

  const handleDateSelect = (start, end) => {
    setStartDate(start);
    setEndDate(end);
  };

  const handleSeuil = (seuil) => {
    setSeuilValeur(seuil);
  };

  return (
    <div className='container-fluid text-dark d-flex p-3 flex-column'>
      <div className='d-flex flex-wrap justify-content-center align-items-center gap-2 p-3 bg-perso-filtre1 rounded'>
        <FiltreCentrale setSelectionCentrale={setSelectionCentrale} AllowAll={false}/>
        <FiltreSeuil onSeuilChange={handleSeuil} />
        <FiltreDate onDateRangeSelect={handleDateSelect} UnselectDate={false} OnDateMode={false} />
        <div className='col-12 d-flex flex-wrap justify-content-center align-items-center gap-2'>
          <button className='btn btn-secondary' onClick={setShowModal}>Categories</button>
          <button onClick={() => setOnlyError(!onlyError)} className="btn-perso btn-perso-primary">
            {onlyError ? 'Afficher Tout' : 'Afficher Erreurs Seulement'}
          </button>
        </div>
      </div>
      <div className="container-fluid mt-3 p-2">
        <Tableau
          SelectCentrale={selectionCentrale}
          start={startDate}
          end={endDate}
          Leseuil={SeuilValeur}
          setClickedData={setClickedData}
          setShowModal={setShowModal}
          onlyError={onlyError}
        />
      </div>
      <CategorisationModal setShowModal={setShowModal} showModal={showModal} ClickedData={ClickedData} setClickedData={setClickedData} Centrale={selectionCentrale}/>
    </div>
  );
}