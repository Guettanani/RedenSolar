import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { FaCheck } from 'react-icons/fa';

import urlAPI from '../../config';


const GrappeEdit = () => {
    const [selectedGrappe, setSelectedGrappe] = useState({});
    const [AllGrappe, setAllGappe] = useState([]);
    const [AllCentrales, setAllCentrales] = useState([]);
    // const [selectedGrappeCentrales, setSelectedGrappeCentrales] = useState([]);

    const handleGrappeChange = (event) => {
        let NewSelectGrappe = event.target.value;
        NewSelectGrappe = AllGrappe.find((grappe) => grappe.nomGrappe === NewSelectGrappe);
        setSelectedGrappe(NewSelectGrappe);
    };

    const generateGrappe = () => {
        let createGrappe = [];
        for (let i = 0; i < 4; i++) {
            createGrappe.push({
                idGrappe: i,
                nomGrappe: 'Grappe ' + i,
                creator: i % 2 === 0 ? 'benoit' : 'nico',
                centrale: (i % 2 === 0 ? [{ nomCentrale: 'Agen Centre' }, { nomCentrale: 'Aguilar 1' }] : [{ nomCentrale: 'Abattoirs de Langogne' }, { nomCentrale: 'Augier 2' }]),
            });
        }
        setAllGappe(createGrappe);
        setSelectedGrappe(createGrappe[0]);
    }

    useEffect(() => {
        generateGrappe();
        fetchCentrales();
        console.log('data ok');
    }, []);

    const fetchCentrales = async () => {
        try {
            const response = await axios.get(urlAPI + "getSelec/", {
                timeout: 5000 // Timeout en millisecondes (par exemple, 5 secondes)
            });
            const responseData = response.data;
            const TempList = [...responseData];
            setAllCentrales(TempList);
            // setSelectCentrale(AllowAll ? 'Toute' : responseData[responseData.length - 1].selected_nom);
        } catch (error) {
            console.log(error);
        }
    };

    const handleCentraleChange = (ClickedCentrale) => {
        console.log(ClickedCentrale);

        // Créez une nouvelle liste de centrales pour la grappe sélectionnée
        const updatedCentrales = selectedGrappe.centrale.map(item => ({ ...item })); // Clonez les centrales existantes
        if (updatedCentrales.some(item => item.nomCentrale === ClickedCentrale)) {
            updatedCentrales.filter(item => item.nomCentrale !== ClickedCentrale)
        } else {
            updatedCentrales.push({ nomCentrale: ClickedCentrale })
        }

        // Mettez à jour la liste des centrales de la grappe sélectionnée
        setSelectedGrappe(prevState => ({
            ...prevState,
            centrale: updatedCentrales
        }));

        console.log(selectedGrappe);
        console.log(selectedGrappe.centrale);
    };


    const handleSubmit = (event) => {
        event.preventDefault();
        // Logique de traitement de la sélection de la grappe et des centrales
        console.log("Grappe sélectionnée :", selectedGrappe);
        console.log("AllGrappe  :", AllGrappe);
        console.log("grappe centrales  :", selectedGrappe.centrale);
    };

    return (
        <div className="container-fluid">
            <div className='d-flex flex-column justify-content-center align-items-center rounded bg-dark p-4 gap-1 text-light'>
                <div className="">
                    <h3 className="display-6">Grappe</h3>
                    <hr />
                </div>
                <form onSubmit={handleSubmit} className='col-10'>
                    <div className="mb-3">
                        <label htmlFor="grappeSelect" className="form-label">Sélectionner une grappe :</label>
                        <select className="form-select" id="grappeSelect" value={selectedGrappe.nomGrappe} onChange={handleGrappeChange}>
                            {/* <option key={800} value="none" >Choisir une grappe</option>
                            <option key={801} value="test">Albioma</option> */}
                            {AllGrappe.map((grappe, index) => (
                                <option key={index} value={grappe.nomGrappe}>{grappe.nomGrappe}</option>
                            ))}
                        </select>
                    </div>
                    {selectedGrappe && (
                        <div className="card mb-3">
                            <div className="card-header">
                                <div className="m-1 p-1">
                                    <h5 className="card-title">Nom :</h5>
                                    <input className='form-control' value={selectedGrappe.nomGrappe}></input>
                                </div>
                                <hr />
                                <div>
                                    <p className="card-text">Créateur :</p>
                                    <input className='form-control' value={selectedGrappe.creator}></input>
                                </div>
                            </div>

                            <div className="card-body">
                                <h6 className="card-subtitle mb-2 text-muted">Centrales:</h6>
                                <ul className="list-group" style={{ maxHeight: '20vh', overflowY: 'scroll' }}>
                                    {AllCentrales
                                        .filter(central => central.nomCentrale) // Filtrer les centrales valides
                                        .map((central, index) => (
                                            <li key={index} className={`list-group-item ${selectedGrappe.centrale && selectedGrappe.centrale.some(item => item.nomCentrale === central.nomCentrale) ? "bg-success" : ""}`} onClick={() => handleCentraleChange(central.nomCentrale)} style={{ cursor: 'pointer' }}>
                                                {selectedGrappe.centrale && selectedGrappe.centrale.some(item => item.nomCentrale === central.nomCentrale) && <FaCheck style={{ marginRight: '5px' }} />}
                                                {central.nomCentrale}
                                            </li>
                                        ))}
                                </ul>

                            </div>

                            {/* Ajoutez ici des champs d'édition pour le contenu de la grappe */}
                            <div className="card-footer">
                                <button type="submit" className="btn btn-primary">Modifier</button>
                            </div>
                        </div>
                    )}
                </form>
            </div>
        </div>
    );
};

export default GrappeEdit;
