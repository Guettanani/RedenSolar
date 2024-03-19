import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { FaCheck } from 'react-icons/fa';

import urlAPI from '../../config';


const GrappeEdit = () => {
    const [selectedGrappe, setSelectedGrappe] = useState({});
    const [AllGrappe, setAllGappe] = useState([]);
    const [AllCentrales, setAllCentrales] = useState([]);
    const [AddGrappe, setAddGrappe] = useState(false);

    const handleGrappeChange = (event) => {
        const selectedValue = event.target.value;
        if (selectedValue === 'New') {
            // Si l'utilisateur choisit d'ajouter une nouvelle grappe, afficher le formulaire d'ajout
            setSelectedGrappe({ nomGrappe: '', creator: '', centrale: [] });
            setAddGrappe(true);
        } else {
            // Sinon, sélectionner la grappe existante
            const selectedGrappe = AllGrappe.find((grappe) => grappe.nomGrappe === selectedValue);
            setSelectedGrappe(selectedGrappe);
            // Masquer le formulaire d'ajout
            setAddGrappe(false);
        }
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
        // console.log('data ok');
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
        // console.log(ClickedCentrale);

        // Créez une nouvelle liste de centrales pour la grappe sélectionnée
        let updatedCentrales = [...selectedGrappe.centrale]; // Clonez les centrales existantes
        if (updatedCentrales.some(item => item.nomCentrale === ClickedCentrale)) {
            updatedCentrales = updatedCentrales.filter(item => item.nomCentrale !== ClickedCentrale); // Retirez la centrale si elle est déjà présente
        } else {
            updatedCentrales.push({ nomCentrale: ClickedCentrale })
        }

        // Mettez à jour la liste des centrales de la grappe sélectionnée
        setSelectedGrappe(prevState => ({
            ...prevState,
            centrale: updatedCentrales
        }));
    };


    const handleSubmit = (event) => {
        event.preventDefault();
        // console.log(event);
        if (AddGrappe) {
            const confirmAdd = window.confirm("Êtes-vous sûr de vouloir ajouter cette grappe ?");
            // Si l'utilisateur confirme la suppression
            if (confirmAdd) {
                // Ajout de la nouvelle grappe dans la grappe selectionné
                setAllGappe([...AllGrappe, selectedGrappe]);
                // Logique d'ajout de la grappe
                console.log("Grappe ajouté :", selectedGrappe);
                console.log("AllGrappe  :", AllGrappe);
            }
        } else {
            const confirmUpdate = window.confirm("Êtes-vous sûr de vouloir modifier cette grappe ?");
            // Si l'utilisateur confirme la suppression
            if (confirmUpdate) {
                // Logique de modification de la grappe
                console.log("Grappe modifiée :", selectedGrappe);
                console.log("AllGrappe  :", AllGrappe);
            }
        }
    };

    const handleDeleteGrappe = () => {
        // Afficher une boîte de dialogue de confirmation
        const confirmDelete = window.confirm("Êtes-vous sûr de vouloir supprimer cette grappe ?");
        // Si l'utilisateur confirme la suppression
        if (confirmDelete) {
            // Logique de suppression de la grappe
            console.log("Grappe supprimée :", selectedGrappe);
            // Filtrer les grappes différentes de la grappe sélectionnée
            const updatedGrappeList = AllGrappe.filter(grappe => grappe.idGrappe !== selectedGrappe.idGrappe);
            // Réinitialiser la liste de toutes les grappes
            setAllGappe(updatedGrappeList);
            // Réinitialiser la sélection de la grappe
            setSelectedGrappe({});
        }
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
                        <select className="form-select" id="grappeSelect" value={AddGrappe ? 'New' : selectedGrappe.nomGrappe} onChange={handleGrappeChange}>
                            {/* <option key={800} value="none" >Choisir une grappe</option>
                            <option key={801} value="test">Albioma</option> */}
                            {AllGrappe.map((grappe, index) => (
                                <option key={index} value={grappe.nomGrappe}>{grappe.nomGrappe}</option>
                            ))}
                            <option value={'New'}>+ Ajouter une nouvelle grappe</option>
                        </select>
                    </div>
                    {selectedGrappe && (
                        <div className="card mb-3">
                            <div className="card-header">
                                <div className="m-1 p-1">
                                    <h5 className="card-title">Nom :</h5>
                                    <input
                                        className='form-control'
                                        name='nomGrappe'
                                        value={selectedGrappe.nomGrappe}
                                        disabled={!AddGrappe}
                                        onChange={(event) => setSelectedGrappe({ ...selectedGrappe, nomGrappe: event.target.value })}
                                    ></input>
                                </div>
                                <hr />
                                <div className="m-1 p-1">
                                    <p className="card-text">Créateur :</p>
                                    <input
                                        className='form-control'
                                        name='creator'
                                        disabled={!AddGrappe}
                                        value={selectedGrappe.creator}
                                        onChange={(event) => setSelectedGrappe({ ...selectedGrappe, creator: event.target.value })}
                                    ></input>
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
                                {!AddGrappe ?
                                    <>
                                        <button type="submit" className="btn btn-primary m-2">Modifier</button>
                                        <button type="button" className="btn btn-danger m-2" onClick={handleDeleteGrappe}>Supprimer</button>
                                    </>
                                    :
                                    <button type="submit" className="btn btn-success m-2">Ajouter</button>

                                }
                            </div>
                        </div>
                    )}
                </form>
            </div>
        </div>
    );
};

export default GrappeEdit;
