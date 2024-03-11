import React, { useEffect, useState } from 'react';
import axios from 'axios';

import 'bootstrap/dist/css/bootstrap.min.css';

import FiltreCentrale from '../Component/CentraleFiltre';
import FiltreYear from '../Component/FiltreYear';

export default function TableauDispo() {
    const today = new Date();
    const [selectionCentrale, setSelectionCentrale] = useState('Abattoirs de Langogne');
    const [selectedYear, setSelectedYear] = useState(today.getFullYear());
    const [contractualAvailability, setContractualAvailability] = useState([]);
    const [data_cate, setData] = useState([])
    // const urlAPI = "http://localhost:8050/";
    const urlAPI = "https://webicamapp.reden.cloud/";

    console.log("data_cate: ", data_cate)


    const chercherDispo = async () => {
        try {
            const response = await axios.get(urlAPI + "getDispo/", {
                params: {
                    selection_centrale: selectionCentrale,
                    annee: selectedYear
                }
            });
            setContractualAvailability(response.data || []);

        } catch (error) {
            console.error("Error fetching disponibilite:", error);
        }
    };
    console.log("contractualAvailability: ", contractualAvailability)

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
        <div className='container-fluid text-dark d-flex p-3 flex-column'>
            <div className='d-flex flex-wrap justify-content-around align-items-center gap-2 p-3 bg-dark rounded text-light'>
                <FiltreCentrale setSelectionCentrale={setSelectionCentrale} AllowAll={false} />
                <FiltreYear SelectedYear={setSelectedYear} />
            </div>

            <div id='container_tab_recap' className='mt-5 container-fluid'>
                <div className='table-responsive overflow-x-scroll d-flex justify-content-center align-items-center'>
                    <table id='tabrecap' className='table table-hover'>
                        <thead>
                            <tr>
                                <th className="cellrecap">Mois</th>
                                <th className="cellrecap">Jan.</th>
                                <th className="cellrecap">Fév.</th>
                                <th className="cellrecap">Mars</th>
                                <th className="cellrecap">Avril</th>
                                <th className="cellrecap">Mai</th>
                                <th className="cellrecap">Juin</th>
                                <th className="cellrecap">Juillet</th>
                                <th className="cellrecap">Août</th>
                                <th className="cellrecap">Sep.</th>
                                <th className="cellrecap">Oct.</th>
                                <th className="cellrecap">Nov.</th>
                                <th className="cellrecap">Dec.</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td className="cellrecap_2">Disponibilité Brute</td>
                                {disponibiliteBrute.map((value, index) => (
                                    <td key={index} className="cellrecap_3">{value !== null ? value : 'N/A'}</td>
                                ))}
                            </tr>
                            <tr>
                                <td className="cellrecap_2">Disponibilité Reden</td>
                                {disponibiliteReden.map((value, index) => (
                                    <td key={index} className="cellrecap_3">{value !== null ? value : 'N/A'}</td>
                                ))}
                            </tr>
                            <tr>
                                <td className="cellrecap_2">Disponibilité Contractuelle</td>
                                {disponibiliteAlbio.map((value, index) => (
                                    <td key={index} className="cellrecap_3">{value !== null ? value : 'N/A'}</td>
                                ))}
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

        </div>
    );
}
