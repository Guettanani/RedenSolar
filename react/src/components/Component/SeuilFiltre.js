import { React, useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';


const FiltreSeuil = ({ onSeuilChange }) => {
  const [seuil, setSeuil] = useState(0);

  const incrementer = () => {
    setSeuil(prevSeuil => prevSeuil + 1);
  };

  const decrementer = () => {
    if (seuil > 0) {
      setSeuil(prevSeuil => prevSeuil - 1);
    }
  };

  const handleSeuilChange = (e) => {
    const newSeuil = parseInt(e.target.value);
    if (!isNaN(newSeuil)) {
      setSeuil(newSeuil);
    }
  };

  useEffect(() => {
    onSeuilChange(seuil);
  }, [seuil]);

  return (
    <div className="col-lg-3 col-4 d-flex flex-wrap align-items-center justify-content-center gap-2">
      <label htmlFor="compteur" className="form-label text-light">Seuil (W)</label>
      <input
        type="number"
        id="compteur"
        className="form-control-sm col-4"
        value={seuil}
        onChange={handleSeuilChange}
      />
      <div id="boutons_compteurs" className="btn-group" role="group">
        <button className="btn btn-primary" onClick={incrementer}>+</button>
        <button className="btn btn-danger" onClick={decrementer}>-</button>
      </div>
    </div>
  );
};

export default FiltreSeuil;
