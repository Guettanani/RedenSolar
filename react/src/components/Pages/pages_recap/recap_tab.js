import React, { useState, useEffect } from 'react';
import './recap_tab.css';
import axios from 'axios';

export default function TabRecap() {
    const today = new Date();
    const [selectedYear, setSelectedYear] = useState(today.getFullYear());
    const [contractualAvailability, setContractualAvailability] = useState([]);


    const selectYear = (direction) => {
        const newYear = direction === 'next' ? selectedYear + 1 : selectedYear - 1;
        setSelectedYear(newYear);
    }

    const chercherDispo = async () => {
        try {
            const response = await axios.get("https://webicamapp.reden.cloud/getDispo/", {
                params: {
                    annee: selectedYear
                }
            });
            setContractualAvailability(response.data|| []);

        } catch (error) {
            console.error("Error fetching disponibilite:", error);
        }
    };
    console.log("contractualAvailability: ",contractualAvailability)

    useEffect(() => {
        chercherDispo();
    }, [selectedYear]);
    
    const disponibiliteBrute = [];
    const disponibiliteReden = [];
    const disponibiliteAlbio = [];

    // Vérifiez si la propriété disponibilites existe dans contractualAvailability
    if (contractualAvailability.disponibilites) {
        // Utilisez map sur disponibilites
        contractualAvailability.disponibilites.forEach((item) => {
            disponibiliteBrute.push(item.disponibilite_brute);
            disponibiliteReden.push(item.disponibilite_reden);
            disponibiliteAlbio.push(item.disponibilite_albio);
        });
    };

    return (
        <div>
            <div id="year-selector">
                <h3>Année</h3>
                <div id="div-buttons">
                    <button onClick={() => selectYear('prev')}>&lt;</button>
                    <p>{selectedYear}</p>
                    <button onClick={() => selectYear('next')}>&gt;</button>
                </div>
            </div>

            <div id='container_tab_recap'>
                <table id='tabrecap'>
                    <thead>
                        <tr>
                            <th id="cellrecap">Mois</th>
                            <th id="cellrecap">Jan.</th>
                            <th id="cellrecap">Fév.</th>
                            <th id="cellrecap">Mars</th>
                            <th id="cellrecap">Avril</th>
                            <th id="cellrecap">Mai</th>
                            <th id="cellrecap">Juin</th>
                            <th id="cellrecap">Juillet</th>
                            <th id="cellrecap">Août</th>
                            <th id="cellrecap">Sep.</th>
                            <th id="cellrecap">Oct.</th>
                            <th id="cellrecap">Nov.</th>
                            <th id="cellrecap">Dec.</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td id="cellrecap_2">Production Réelle</td></tr>
                        <tr><td id="cellrecap_2">Production Attendue</td></tr>
                        <tr><td id="cellrecap_2">Performance Ratio Réelle</td></tr>
                        <tr><td id="cellrecap_2">Performance Ratio Brute</td></tr>
                        <tr><td id="cellrecap_2">Production Ratio attendu</td></tr>
                        <tr>
                            <td id="cellrecap_2">Disponibilité Brute</td>
                            {disponibiliteBrute.map((value, index) => (
                                <td key={index} id="cellrecap_3">{value !== null ? value : 'N/A'}</td>
                            ))}
                        </tr>
                        <tr>
                            <td id="cellrecap_2">Disponibilité Reden</td>
                            {disponibiliteReden.map((value, index) => (
                                <td key={index} id="cellrecap_3">{value !== null ? value : 'N/A'}</td>
                            ))}
                        </tr>
                        <tr>
                            <td id="cellrecap_2">Disponibilité Contractuelle</td>
                            {disponibiliteAlbio.map((value, index) => (
                                <td key={index} id="cellrecap_3">{value !== null ? value : 'N/A'}</td>
                            ))}
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    );
}