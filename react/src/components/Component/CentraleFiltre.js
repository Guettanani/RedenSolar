import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

const FiltreCentrale = ({ setSelectionCentrale, AllowAll }) => {
    const [CentraleList, setCentraleList] = useState([]);
    const [SelectCentrale, setSelectCentrale] = useState(AllowAll ? 'Toute' : 'Abattoirs de Langogne');
    const urlAPI = "https://icamapp.reden.cloud/";


    useEffect(() => {
        remplissage_selec();
    }, []);
    useEffect(() => {
        setSelectionCentrale(SelectCentrale);
    }, [SelectCentrale]);

    const remplissage_selec = async () => {
        try {
            const response = await axios.get(urlAPI + "/getSelec/", {
                timeout: 5000 // Timeout en millisecondes (par exemple, 5 secondes)
            });
            const responseData = response.data;
            const TempList = [{ nomCentrale: "Toute" }, ...responseData];
            setCentraleList(TempList);
            setSelectCentrale(AllowAll ? 'Toute' : responseData[responseData.length - 1].selected_nom);
        } catch (error) {
            console.log(error);
        }
    };


    const changement_centrale = async (e) => {
        const newSelectionCentral = e.target.value;
        setSelectCentrale(newSelectionCentral);
    };

    return (
        <div className="col-lg-5 col-4 d-flex flex-column">
            <label htmlFor="filtre_centrale" className="form-label text-light">Centrale:</label>
            <select
                className='form-select-sm'
                style={{ maxHeight: '50px' }}
                id='filtre_centrale'
                value={SelectCentrale}
                onChange={changement_centrale}
            >
                {CentraleList.map((item) => (
                    (item.nomCentrale) ?
                        <option key={item.nomCentrale} value={item.nomCentrale}>
                            {item.nomCentrale}
                        </option>
                        : null
                ))}
            </select>
        </div>
    );
};

export default FiltreCentrale;
