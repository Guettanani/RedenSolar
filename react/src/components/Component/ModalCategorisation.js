import React, { useState } from 'react';
import axios from 'axios'; // Importer axios si ce n'est pas déjà fait

import 'bootstrap/dist/css/bootstrap.min.css';

const CategorisationModal = ({ setShowModal, showModal, ClickedData, setClickedData,Centrale }) => {
    const [categorieSelectionnee, setCategorieSelectionnee] = useState('');
    const [Description, setDescription] = useState('');

    const handleCloseModal = () => {
        setShowModal(false);
    };

    function formatDateIso(dateIso) {
        // Créer un objet Date à partir de la date ISO
        const date = new Date(dateIso);

        // Options de formatage
        const options = {
            year: "numeric",
            month: "numeric",
            day: "numeric",
            hour: "numeric",
            minute: "numeric",
            second: "numeric",
            hour12: false,
            timeZone: "UTC",
        };

        // Formater la date
        const formattedDate = date.toLocaleDateString("fr-FR", options);

        // Retourner la date formatée
        return formattedDate;
    }

    const SaveMainCourante = async () => {
        try {
            // console.log('ClickedData:', ClickedData);

            //List that contain all the equipement of clickeddata.nomReference 
            const ListEquipement = [...new Set(ClickedData.map(item => item.nomReference))];
            //A filter that eliminate all the duplicated equipement in the list
            const ListEquipementFilter = ListEquipement.filter((item, index) => ListEquipement.indexOf(item) === index);
            // Convert the list of equipment into a comma-separated string
            const EquipementString = ListEquipementFilter.join(', ');

            const premierElement = ClickedData.reduce((prev, current) => (prev.temps < current.temps ? prev : current)).temps;
            const dernierElement = ClickedData.reduce((prev, current) => (prev.temps > current.temps ? prev : current)).temps;

            const data = {
                iddefaut: categorieSelectionnee,
                idheuredebut: formatDateIso(premierElement),
                idheurefin: formatDateIso(dernierElement),
                idcommentaires: Description,
                idequipementEndommage: EquipementString,
                idcentrale: Centrale,
            };
            console.log(data);

            // Send data to the server using Axios
            const response = await axios.post('http://localhost:8050/ajouter_article/', data);

            if (response.status === 200) {
                console.log(`Article ajouté avec succès pour les equipements ${ListEquipement}.`);
            } else {
                console.error(`Erreur lors de l'ajout de l'article pour les équipements ${ListEquipement}.`);
            }

            setClickedData([]);
        } catch (error) {
            console.error("Erreur lors de la requête POST :", error);
        }

    };

    const handleSave = () => {
        // Close the modal when the save button is clicked
        handleCloseModal();
        // Log the clicked data to the console
        console.log(ClickedData);
        // Check if any data was clicked
        if (ClickedData.length === 0) {
            // Alert the user to select data
            alert("Veuillez sélectionner des données à catégoriser");
        } else if (categorieSelectionnee === '') {
            // Alert the user to select a default category
            alert("Veuillez sélectionner une catégorie de défaut");
            // Show the modal
            setShowModal(true);
        }
        else {
            SaveMainCourante();
            // Create a string with the clicked data
            alert(`Une nouvelle main courante c'est créer avec les informations suivante :
            ${ClickedData.length > 2
                    ?
                    `\nDate : ${ClickedData[0].DateTimeClick} => ${ClickedData[ClickedData.length - 1].DateTimeClick}
                \nEquipement : ${ClickedData[0].OnduleurClick.nomReference} => ${ClickedData[ClickedData.length - 1].OnduleurClick.nomReference}
                \nType d'arret : ${categorieSelectionnee}`
                    : `\nDate :${ClickedData[0].DateTimeClick} 
                    \nEquipement : ${ClickedData[0].OnduleurClick.nomReference}
                    \nType d'arret : ${categorieSelectionnee}`
                }
            `);
        }

    };

    const CategorisationData = [
        { texte: 'Découplage' },
        { texte: 'Sinistre' },
        { texte: 'Travaux ENEDIS' },
        { texte: 'Curratif' },
        { texte: 'Défaut Riso Module' },
        { texte: 'Préventif' },
        { texte: 'Attente Pièces' },
        { texte: 'Ombrage' },
        { texte: 'Communication' },
    ];


    return (
        showModal && (
            <div
                className="modal fade show d-block"
                tabIndex="-1"
                role="dialog"
                aria-labelledby="CategorisationModalLabel"
                aria-hidden="true"
            >
                <div className="modal-dialog modal-dialog-centered" role="document">
                    <div className="modal-content">
                        <div className="modal-header">
                            <h5 className="modal-title" id="CategorisationModalLabel">
                                Categorisation
                            </h5>
                            <button
                                type="button"
                                className="btn-close"
                                data-bs-dismiss="modal"
                                aria-label="Close"
                                onClick={handleCloseModal}
                            />
                        </div>
                        <div className="modal-body">
                            <label htmlFor="categorie">Catégorie:</label>
                            <select
                                id="categorie"
                                className="form-select mb-3"
                                value={categorieSelectionnee}
                                onChange={(e) => setCategorieSelectionnee(e.target.value)}
                            >
                                {CategorisationData.map((categorie) => (
                                    <option key={categorie.texte} value={categorie.texte}>
                                        {categorie.texte}
                                    </option>
                                ))}
                            </select>

                            <label htmlFor="description">Description:</label>
                            <textarea
                                id="description"
                                className="form-control"
                                placeholder="Rajouter une description pour compléter les information sur l'arret"
                                onChange={(e) => setDescription(e.target.value)}
                            />
                        </div>

                        <div className="modal-footer">
                            <button
                                type="button"
                                className="btn btn-secondary"
                                data-bs-dismiss="modal"
                                onClick={handleCloseModal}

                            >
                                Annuler
                            </button>
                            <button
                                type="button"
                                className="btn btn-primary"
                                onClick={handleSave}
                            >
                                Valider
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        )
    );
};

export default CategorisationModal;
