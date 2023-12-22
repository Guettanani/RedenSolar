import React, { useEffect, useState } from 'react';
import './main_courante.css';
import axios from 'axios';
export default function TstTab() {
    const [data, setData] = useState([]);
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get("http://localhost:8050/data/");
                const responseData = response.data;
                setData(responseData);
                console.log(responseData);
            } catch (error) {
                console.error("Une erreur s'est produite : ", error);
            }
        };

        fetchData();
    }, []);
    const formatDate = (dateString) => {
        const options = { year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric',timeZone: 'UTC', };
        return new Date(dateString).toLocaleDateString('fr-FR', options);
    };
    return(
        <div id="tab_container_mc">
            <table id="tab_mc" >
                <thead id="head_container">
                    <th id="head_mc">Type de défaut</th>
                    <th id="head_mc">Date et Heure de Début</th>
                    <th id="head_mc">Date et Heure de fin</th>
                    <th id="head_mc">centrale</th>
                    <th id="head_mc">équipement impacté</th>
                    <th id="head_mc">Description</th>
                </thead>
                <tbody>
                    
                {data.map((item, index) => {
                    return (
                        <tr key={index}>
                        <td id="head_mc">{item.iddefaut}</td> 
                        <td id="head_mc">
                        {formatDate(item.idheuredebut)}                        
                        </td> 
                        <td id="head_mc">
                        {formatDate(item.idheurefin)}                            
                        </td>
                        <td id="head_mc">{item.idcentrale}</td>
                        <td id="head_mc">{item.idequipementEndommage}</td>
                        <td id="head_mc">{item.idcommentaires}</td>
                        </tr>
                    );
                    })}


                </tbody>

            </table>
        </div>
    );
}