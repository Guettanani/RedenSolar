import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../../App.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEdit, faTrash } from '@fortawesome/free-solid-svg-icons';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import urlAPI from '../../config';


const TableMainCourante = ({ startDate, endDate, SelectedCentrale, DateMode }) => {
    const [data, setData] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [selectedItem, setSelectedItem] = useState(null);
    // const urlAPI = "http://localhost:8050/";
    // const urlAPI = "https://webicamapp.reden.cloud/";

    const fetchData = async () => {
        try {
            const response = await axios.get(urlAPI + 'data/');
            const responseData = response.data;
            let filteredData = responseData;

            if (responseData &&  SelectedCentrale !== 'Toute' && SelectedCentrale !== null) {
                filteredData = responseData.filter(item => item.idcentrale === SelectedCentrale);
            }

            if (responseData && DateMode !== 'none' && DateMode !== null) {
                filteredData = filteredData.filter(item => item.idheuredebut >= startDate && item.idheurefin <= endDate);
            }

            setData(filteredData);
        } catch (error) {
            console.error("Une erreur s'est produite : ", error);
        }
    };

    const deleteMC = async (item) => {
        try {
            await axios.delete(urlAPI + 'deleteMC/', { data: item });
            fetchData();
        } catch (error) {
            console.error("Erreur lors de la suppression : ", error);
        }
    };

    const openModal = (item) => {
        setSelectedItem(item);
        setShowModal(true);
    };

    const closeModal = () => {
        setSelectedItem(null);
        setShowModal(false);
    };

    const handleFormSubmit = async (formData) => {
        try {
            // Envoyer une requête pour mettre à jour les données sur le serveur avec les nouvelles données du formulaire
            console.log("Nouvelles données du formulaire : ", formData);
            // Une fois la mise à jour réussie, fermer le modal et rafraîchir les données
            closeModal();
            fetchData();
        } catch (error) {
            console.error("Erreur lors de la mise à jour : ", error);
        }
    };

    useEffect(() => {
        fetchData();
    }, [SelectedCentrale, startDate, endDate]);

    useEffect(() => {
        fetchData();
    }, []);

    return (
        <div id="tab_container_mc" className='col-12 overflow-x-scroll'>
            <table id="tab_mc" className='table table-hover text-center table-responsive'>
                <thead id="head_container">
                    <tr>
                        <th>Type de défaut</th>
                        <th>Date et Heure de Début</th>
                        <th>Date et Heure de fin</th>
                        <th>centrale</th>
                        <th>équipement impacté</th>
                        <th>Description</th>
                        <th>Outils</th>
                    </tr>
                </thead>
                <tbody>
                    {data && data.map((item, index) => (
                        <tr key={index}>
                            <td className='table-danger-perso'>{item.iddefaut}</td>
                            <td className='table-info-perso'>{item.idheuredebut}</td>
                            <td className='table-info-perso'>{item.idheurefin}</td>
                            <td>{item.idcentrale}</td>
                            <td>{item.idequipementEndommage}</td>
                            <td>{item.idcommentaires}</td>
                            <td className='d-flex flex-wrap justify-content-center align-items-center gap-2'>
                                <button
                                    className='btn btn-outline-danger'
                                    onClick={() => deleteMC(item)}
                                >
                                    <FontAwesomeIcon icon={faTrash} />
                                </button>
                                <button
                                    className='btn btn-outline-secondary'
                                    onClick={() => openModal(item)}
                                >
                                    <FontAwesomeIcon icon={faEdit} />
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {/* Modal pour la modification */}
            <Modal show={showModal} onHide={closeModal}>
                <Modal.Header closeButton>
                    <Modal.Title>Modifier la donnée de main-courante</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <form onSubmit={handleFormSubmit} className='d-flex flex-column justify-content-center align-items-center gap-2'>
                        <div className="form-group">
                            <label htmlFor="iddefaut">Type de défaut</label>
                            <input type="text" className="form-control" id="iddefaut" defaultValue={selectedItem?.iddefaut} />
                        </div>
                        <div className="form-group">
                            <label htmlFor="idheuredebut">Date et Heure de Début</label>
                            <input type="datetime-local" className="form-control" id="idheuredebut" defaultValue={selectedItem?.idheuredebut ? new Date(selectedItem.idheuredebut).toISOString().substring(0, 16) : ''} />
                        </div>
                        <div className="form-group">
                            <label htmlFor="idheurefin">Date et Heure de fin</label>
                            <input type="datetime-local" className="form-control" id="idheurefin" defaultValue={selectedItem?.idheurefin ? new Date(selectedItem.idheurefin).toISOString().substring(0, 16) : ''} />
                        </div>
                        <div className="form-group">
                            <label htmlFor="idcentrale">Centrale</label>
                            <input type="text" className="form-control" id="idcentrale" defaultValue={selectedItem?.idcentrale} />
                        </div>
                        <div className="form-group">
                            <label htmlFor="idequipementEndommage">Équipement endommagé</label>
                            <input type="text" className="form-control" id="idequipementEndommage" defaultValue={selectedItem?.idequipementEndommage} />
                        </div>
                        <div className="form-group">
                            <label htmlFor="idcommentaires">Commentaires</label>
                            <textarea className="form-control" id="idcommentaires" defaultValue={selectedItem?.idcommentaires}></textarea>
                        </div>
                        <Button variant="primary" type="submit">
                            Valider
                        </Button>
                    </form>
                </Modal.Body>
            </Modal>
        </div>
    );
};

export default TableMainCourante;
