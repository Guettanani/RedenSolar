import React, { useEffect, useState } from 'react';
import './main_courante.css';
import axios from 'axios';

export default function TstTab() {
    const [data, setData] = useState([]);
    const fetchData = async () => {
        try {
            const response = await axios.get("https://webicamapp.reden.cloud/data/");
            const responseData = response.data;
            setData(responseData);
            console.log(responseData);
        } catch (error) {
            console.error("Une erreur s'est produite : ", error);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const formatDate = (dateString) => {
        const options = { year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric', timeZone: 'UTC' };
        return new Date(dateString).toLocaleDateString('fr-FR', options);
    };

    const deleteMC = async (item) => {
        try {
            console.log("item: ",item)
            // Faites une requête DELETE à votre API avec toutes les données de la ligne
            await axios.delete("https://webicamapp.reden.cloud/deleteMC/", { data: item });
            // Rafraîchissez les données après la suppression
            fetchData()

        } catch (error) {
            console.error("Erreur lors de la suppression : ", error);
        }
    };

    return (
        <div id="tab_container_mc">
            <table id="tab_mc">
                <thead id="head_container">
                    <th id="head_mc">Type de défaut</th>
                    <th id="head_mc">Date et Heure de Début</th>
                    <th id="head_mc">Date et Heure de fin</th>
                    <th id="head_mc">centrale</th>
                    <th id="head_mc">équipement impacté</th>
                    <th id="head_mc">Description</th>
                    <th id="head_mc">Supprimer</th>
                </thead>
                <tbody>
                    {data.map((item, index) => {
                        return (
                            <tr key={index}>
                                <td id="head_mc">{item.iddefaut}</td>
                                <td id="head_mc">{formatDate(item.idheuredebut)}</td>
                                <td id="head_mc">{formatDate(item.idheurefin)}</td>
                                <td id="head_mc">{item.idcentrale}</td>
                                <td id="head_mc">{item.idequipementEndommage}</td>
                                <td id="head_mc">{item.idcommentaires}</td>
                                <td id="head_mc">
                                    <button onClick={() => deleteMC(item)}>X</button>
                                </td>
                            </tr>
                        );
                    })}
                </tbody>
            </table>
        </div>
    );
}