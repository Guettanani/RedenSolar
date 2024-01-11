import React, { useEffect, useState } from 'react';
import './main_courante.css';
import axios from 'axios';

export default function TstTab() {
    const [data, setData] = useState([]);
    const [selectionCentrale, setSelectionCentrale] = useState()
    const [data_cate, setDataCate]=useState([])

    useEffect(() => {
        remplissage_selec();
      }, []);
    

    const remplissage_selec = async() => {
        try{
          const response = await axios.get("http://localhost:8050/getSelec/")
        
          const responseData = response.data;
          setDataCate(responseData)
          console.log("responseData: ",responseData.selected_nom)
          setSelectionCentrale(responseData[responseData.length - 1].selected_nom)
        }catch(error){ console.log(error)}
        }
        console.log("data_cate: ",data_cate)

    const fetchData = async () => {
        try {
            console.log("Valeur actuelle de selectionCentrale dans fetchData : ", selectionCentrale);

            const response = await axios.get("http://localhost:8050/data/");
            const responseData = response.data;
            console.log('responseData: ',responseData)
            console.log('selectionCentrale: ',selectionCentrale)
            if (selectionCentrale!=='Toutes')
                {const filteredData = responseData.filter(item => item.idcentrale === selectionCentrale);
                console.log('filteredData: ',filteredData)
                setData(filteredData);}
            else{
                setData(responseData)
            }
            console.log(responseData);
        } catch (error) {
            console.error("Une erreur s'est produite : ", error);
        }
    };

    useEffect(() => {
        fetchData();
    }, [selectionCentrale]);

    const formatDate = (dateString) => {
        const options = { year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric', timeZone: 'UTC' };
        return new Date(dateString).toLocaleDateString('fr-FR', options);
    };

    const deleteMC = async (item) => {
        try {
            console.log("item: ",item)
            // Faites une requête DELETE à votre API avec toutes les données de la ligne
            await axios.delete("http://localhost:8050/deleteMC/", { data: item });
            // Rafraîchissez les données après la suppression
            fetchData()

        } catch (error) {
            console.error("Erreur lors de la suppression : ", error);
        }
    };
    const changement_centrale = async (e) => {
        const newSelectionCentral = e.target.value;
      
        try {
            console.log("Nouvelle centrale sélectionnée : ", newSelectionCentral);

          const response = await axios.get("http://localhost:8050/getCentrale_2/", {
            params: {
              selected_nom: newSelectionCentral,
            }
          });
      
          const responseData = response.data;
          console.log(responseData)
          setSelectionCentrale(newSelectionCentral);
          fetchData(selectionCentrale);
        } catch (error) {
          console.error("Une erreur s'est produite : ", error);
        }
      };

    return (
        <div>            
            <select id='filtre_centrale' value={selectionCentrale} onChange={changement_centrale}>
                <option>Toutes</option>
                {data_cate.map((item) =>(<option id="selec_centrale">{item.nomCentrale}</option>))}
            </select>
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
        </div>
    );
}