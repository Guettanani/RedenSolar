import { React, useState, useEffect,useRef} from 'react';
import './categories.css';
import axios from 'axios';
import Calendar from './Calendar';


export default function Categories(){

  const today = new Date();
  const oneWeekAgo = new Date(today);
  oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);  
  const [selectedRowIndex, setSelectedRowIndex] = useState();
  const [dataToMc, setDataToMc] = useState(null);
  const[selectionCentrale,newSelectionCentrale] = useState('Abattoirs de Langogne');
  const [data, setData] = useState([]);
  const[data_cate, setDataCate]=useState([])
  const [compteur, setCompteur] = useState(0);
  const [startDate, setStartDate] = useState(oneWeekAgo.toISOString().split('T')[0]);
  const [endDate, setEndDate] = useState(today.toISOString().split('T')[0]);
  const [secondOverlayPosition, setSecondOverlayPosition] = useState({ top: 0, left: 0 });
  const [selectedPeriod, setSelectedPeriod] = useState("1 semaine");
  const [showCalendarOverlay, setShowCalendarOverlay] = useState(false);
  const [periodSelectorPosition, setPeriodSelectorPosition] = useState({ top: 0, left: 0 });
  const initialSelectionCentrale = useRef(null);
  const [isChecked, setIsChecked] = useState(false);
  const [valeurDispo, setValeurDispo]= useState(null);

const cherhcer_dispo = async () => {
  try {
    const response = await axios.get("https://webicamapp.reden.cloud/getDispo/", {
      params: {
        selected_nom: initialSelectionCentrale.current,
        date_debut: startDate,
        date_fin: endDate
      }
    });
    setValeurDispo(response.data.disponibilite);
  } catch (error) {
    console.error("Error fetching disponibilite:", error);
    // Handle the error, you might want to set an error state or display an error message
  }
};

  // const check_show = () => {
  //   const allCells = document.querySelectorAll('#tab_cate .tab_h');
  //   const zeroValueCells = document.querySelectorAll('#tab_cate .zero-value');
  
  //   if (isChecked) {
  //     // Afficher uniquement les cellules de la classe "zero-value"
  //     allCells.forEach(cell => cell.classList.add('hidden-cell'));
  //     zeroValueCells.forEach(cell => cell.classList.remove('hidden-cell'));
  //     console.log("oui");
  //   } else {
  //     // Afficher toutes les cellules
  //     allCells.forEach(cell => cell.classList.remove('hidden-cell'));
  //   }
  // };

  const handleCheckboxChange = () => {
    setIsChecked(!isChecked);
  };
  // useEffect(()=> {
  //   check_show()
  // })
  
  useEffect(() => {
    remplissage_selec();
  }, []);
  useEffect(() => {
    initialSelectionCentrale.current = selectionCentrale;
  }, [selectionCentrale]);
  useEffect(() => {
    fetchdatacentrale();
  }, [startDate, endDate]);
  useEffect(()=> {
    cherhcer_dispo()
  })
  useEffect(() => {
    fetchdatacentrale();
  }, [selectionCentrale]);
  console.log(valeurDispo)


  const handleDateSelect = (date) => {
    console.log('Date sélectionnée dans Categories:', date);
  
    if (date) {
      setStartDate(date.toISOString().split('T')[0]);
      console.log('Date de début :', date.toISOString().split('T')[0]);
    } else {
      setStartDate(null);
    }
    
  };
  
  const handleEndDateSelect = (date) => {
    console.log('Date de fin sélectionnée dans Categories:', date);
  
    if (date) {
      setEndDate(date.toISOString().split('T')[0]);
      console.log('Date de fin :', date.toISOString().split('T')[0]);
    } else {
      setEndDate(null);
    }
    
  };
  

  const handlePeriodChange = (e) => {
    const selectedValue = e.target.value;
    setSelectedPeriod(selectedValue);
    console.log(selectedPeriod)
    const periodSelector = document.getElementById("select-period");
    const position = periodSelector.getBoundingClientRect();
    setPeriodSelectorPosition({
      top: position.top + window.scrollY,
      left: position.left + window.scrollX,
    });
  
    if (selectedValue === "autre") {
      setShowCalendarOverlay(true);
    } else {
      setShowCalendarOverlay(false);
    }
    if (selectedValue === "1 semaine") {
      const today = new Date();
      const oneWeekAgo = new Date(today);
      oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
      setStartDate(oneWeekAgo.toISOString().split('T')[0]);
      
      
      setEndDate(today.toISOString().split('T')[0]);
      
    }
    else if (selectedValue === "2 semaines") {
      const today = new Date();
      const oneWeekAgo = new Date(today);
      oneWeekAgo.setDate(oneWeekAgo.getDate() - 14);
      setStartDate(oneWeekAgo.toISOString().split('T')[0]);
      console.log("startDate: ",startDate)
      
      setEndDate(today.toISOString().split('T')[0]);
      console.log("endDate: ",endDate)
    }
    else if (selectedValue === "1 mois") {
      const today = new Date();
      const oneWeekAgo = new Date(today);
      oneWeekAgo.setDate(oneWeekAgo.getDate() - 31);
      setStartDate(oneWeekAgo.toISOString().split('T')[0]);
      console.log("startDate: ",startDate)
      
      setEndDate(today.toISOString().split('T')[0]);
      console.log("endDate: ",endDate)
    }
  };

  const incrementer = () => {
    try {
      setCompteur((prevCompteur) => prevCompteur + 1); 
    } catch (error) {
      console.log(error);
    }
  };

  const decrementer = () => {
    if(compteur!==0){
    try {
      setCompteur((prevCompteur) => prevCompteur - 1); 
    } catch (error) {
      console.log(error);
    }
    console.log(compteur)
  }
  };
  

const remplissage_selec = async() => {
try{
  const response = await axios.get("https://webicamapp.reden.cloud/getSelec/")

  const responseData = response.data;
  setDataCate(responseData);
}catch(error){ console.log(error)}

}


const formatDate = (dateString) => {
  const options = {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    timeZone: 'UTC',
  };

  const date = new Date(dateString);
  const formattedDate = date.toLocaleDateString('fr-FR', options);
  return formattedDate;
};
  
  const fetchdatacentrale = async () =>{
      try {
        const response = await axios.get("https://webicamapp.reden.cloud/getCentrale/", {
                params: {
                    selected_nom: initialSelectionCentrale.current,
                    date_debut: startDate,
                    date_fin: endDate
                }
            });
          // console.log(selectionCentrale)
        const responseData = response.data;
        setData(responseData);
        // console.log(responseData);
    } catch (error) {
        console.error("Une erreur s'est produite : ", error);
    }

  }

  const changement_centrale = async (e) => {
    const newSelectionCentral = e.target.value;

    try {
      const response = await axios.get("https://webicamapp.reden.cloud/getCentrale/", {
        params: {
          selected_nom: newSelectionCentral,
          date_debut: startDate,
          date_fin: endDate
        }
      });

      const responseData = response.data;
      setData(responseData);
      newSelectionCentrale(newSelectionCentral);
    } catch (error) {
      console.error("Une erreur s'est produite : ", error);
    }
  }
  console.log(data)

  

  const ouvrir_overlay_2 = (index) => {
    setSecondOverlayVisible(true);
    setSelectedRowIndex(index);

    setSecondOverlayPosition({
      top: positionMenu.top,
      left: positionMenu.left +10, 
    });
  };
  const envoi_categorisation =( valeur) => {
    if (valeur=== 'annuler') {
      setSecondOverlayVisible(false);
    } else if (valeur==='confirmer') {
      setSecondOverlayVisible(false);
      effectuerRequetePost(selectedRowIndex);
    }
  };
  const effectuerRequetePost = async (selectedRowIndex) => {

    try {
      const ligne = donnees[selectedRowIndex];
      const texteDeLaColonneCorrespondante = ligne.texte;
      const uniqueColumns = Array.from(new Set(clickedRows.map(item => item.colonne)));
      const commentaire = document.getElementById('ameliorer').value;
      const centrale = selectionCentrale;
  
      if (texteDeLaColonneCorrespondante === 'Découplage' || texteDeLaColonneCorrespondante === 'Travaux ENEDIS') {
        const idequipementEndommage = uniqueColumns.join(', ');

        const dates = clickedRows.map(item => ({
          date: formatDate(item.dateColonne),
          heure: item.heureColonne,
        }));
        
        dates.sort((a, b) => {
          const dateA = new Date(`${a.date} ${a.heure}`);
          const dateB = new Date(`${b.date} ${b.heure}`);
          return dateA - dateB;
        });
        
  
        const premierElement = dates[0];
        const dernierElement = dates[dates.length - 1];
        const data = {
          iddefaut: texteDeLaColonneCorrespondante,
          idheuredebut: premierElement.date,
          idheurefin: dernierElement.date,
          idcommentaires: commentaire,
          idequipementEndommage: idequipementEndommage,
          idcentrale: centrale,
        };
  
        const response = await axios.post('https://webicamapp.reden.cloud/ajouter_article/', data);
        if (response.status === 200) {
          console.log(`Article ajouté avec succès pour la colonne ${idequipementEndommage}.`);
        } else {
          console.error(`Erreur lors de l'ajout de l'article pour la colonne ${idequipementEndommage}.`);
        }
      } else {
        for (const columnName of uniqueColumns) {
          const rowsForColumn = clickedRows.filter(item => item.colonne === columnName);
  
          // Triez les lignes par date et heure (créez une copie triée)
          // console.log('Rows avant tri pour la colonne', columnName, ':', rowsForColumn);

          // Triez les lignes par date et heure (créez une copie triée)
          const sortedRows = rowsForColumn.slice().sort((a, b) => {
            const datetimeA = new Date(`${a.dateColonne} ${a.heureColonne}`);
            const datetimeB = new Date(`${b.dateColonne} ${b.heureColonne}`);
            return datetimeA - datetimeB;
          });
  

  
          const premierElement = sortedRows[0];
          const dernierElement = sortedRows.length > 1 ? sortedRows.pop() : premierElement;

          const data = {
            iddefaut: texteDeLaColonneCorrespondante,
            idheuredebut: `${premierElement.dateColonne} ${premierElement.heureColonne}`,
            idheurefin: `${dernierElement.dateColonne} ${dernierElement.heureColonne}`,
            idcommentaires: commentaire,
            idequipementEndommage: columnName,
            idcentrale: centrale,
          };
  

          const response = await axios.post('https://webicamapp.reden.cloud/ajouter_article/', data);
  
          if (response.status === 200) {
            console.log(`Article ajouté avec succès pour la colonne ${columnName}.`);
          } else {
            console.error(`Erreur lors de l'ajout de l'article pour la colonne ${columnName}.`);
          }
        }
      }
  
      setDataToMc(null);
      setClickedRows([]);
      setSelectedRowIndex([]);
      setMenuVisible(false);
    } catch (error) {
      console.error("Erreur lors de la requête POST :", error);
    }
  };
  
 
  const [secondOverlayVisible, setSecondOverlayVisible] = useState(false);
  const [clickedRows, setClickedRows] = useState([]);


  function objectsEqual(obj1, obj2) {
    const keys1 = Object.keys(obj1);
    const keys2 = Object.keys(obj2);
  
    if (keys1.length !== keys2.length) return false;
  
    for (let key of keys1) {
      if (obj1[key] !== obj2[key]) return false;
    }
  
    return true;
  }
  const click_on_line = (e, rowIndex, cellIndex) => {
    console.log("Clic détecté :", rowIndex, cellIndex);
    const celll= cellIndex+2
    if (celll>=2) {
      const columnName = document.querySelectorAll('#tab_cate th')[celll].textContent;

      const texteColonne1 = document.querySelectorAll('#tab_cate tbody tr')[rowIndex].querySelector('td:first-child').textContent;


      const heureColonne = texteColonne1.substring(11, 16);
  
      const dateColonne =texteColonne1.substring(0, 10);
  
      const colonne = columnName;
  
      const liste_donnees = { rowIndex, celll, colonne, heureColonne, dateColonne };

  
      const isSelected = clickedRows.some((item) => objectsEqual(item, liste_donnees));
  
      if (isSelected) {
        setClickedRows(clickedRows.filter((item) => !objectsEqual(item, liste_donnees)));
        setSelectedRowIndex(null);
      } else {
        setClickedRows([...clickedRows, liste_donnees]);
        setSelectedRowIndex(rowIndex);
      }
    }
    else if (!cellIndex){
      selectAllCellsForRow(rowIndex);
    }
  };
  console.log(clickedRows)

  const selectAllCellsForRow = (rowIndex) => {

    const rowColumns = document.querySelectorAll(`#tab_cate tbody tr:nth-child(${rowIndex + 1}) td`);
    const headerCells = document.querySelectorAll('#tab_cate th');

    const selectedCells = [];
    const texteColonne1 = rowColumns[0].textContent;
    console.log("texteColonne1: ",texteColonne1)
    const heureColonne = texteColonne1.substring(11, 16);
    const dateColonne = texteColonne1.substring(0, 10);
    
  
    Array.from(rowColumns).forEach((cell, index) => {
      const cellIndex = index + 2;
      const celll = cellIndex;

      if (cellIndex >= 2 && cellIndex < headerCells.length) {
        const columnName = headerCells[cellIndex].textContent;
  

        if (columnName !== undefined) {
    
          
          const colonne = columnName;
  
          const liste_donnees = { rowIndex, celll, colonne, heureColonne, dateColonne };
          selectedCells.push(liste_donnees);
        } else {
          console.error(`Le nom de la colonne pour l'index ${cellIndex} est undefined.`);
        }
      } else {
        console.error(`L'index de colonne ${cellIndex} est hors des limites.`);
      }
    });
  
    const isRowSelected = clickedRows.some((item) => item.rowIndex === rowIndex);
  
    if (isRowSelected) {

      setClickedRows(clickedRows.filter((item) => item.rowIndex !== rowIndex));
      setSelectedRowIndex(null);
    } else {

      setClickedRows([...clickedRows, ...selectedCells]);
      setSelectedRowIndex(rowIndex);
    }
  };


  

    const [menuVisible, setMenuVisible] = useState(false);
    const [positionMenu, setPositionMenu] = useState({ top: 0, left: 0 });


    const handleContextMenu = (e) => {
    e.preventDefault(); 
    const offsetX = e.clientX-300;
    const offsetY = e.clientY-100;
    console.log("offsetX: ",offsetX)
    console.log("offsetY: ",offsetY)

    setPositionMenu({ top: offsetY, left: offsetX });
    setMenuVisible(true);
  };

  const close_overlay_1 = ()=>{
    setMenuVisible(false);
    if (secondOverlayVisible===true){
      setSecondOverlayVisible(false)
    }
  };
  
  const donnees = [
    { texte: 'Découplage', boutonTexte: 'Valider' },
    { texte: 'Sinistre', boutonTexte: 'Valider' },
    { texte: 'Travaux ENEDIS', boutonTexte: 'Valider' },
    { texte: 'Curratif', boutonTexte: 'Valider' },
    { texte: 'Défaut Riso Module', boutonTexte: 'Valider' },
    { texte: 'Préventif', boutonTexte: 'Valider' },
    { texte: 'Attente Pièces', boutonTexte: 'Valider' },
    { texte: 'Ombrage', boutonTexte: 'Valider' },
    { texte: 'Communication', boutonTexte: 'Valider' },
  ];

  const generateTableHeader = () => {
    return (
      <thead>
        <tr>
          <th>Date</th>

          <th>Irradiance</th>
          {data.map((item) => (
            <th key={item.nomReference}>
              {item.nomReference}
            </th>
          ))}
        </tr>
      </thead>
    );
  };

  const close_calendar = () => {
    setShowCalendarOverlay(false)
    setSelectedPeriod("1 semaine");
    const today = new Date();
      const oneWeekAgo = new Date(today);
      oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
      setStartDate(oneWeekAgo.toISOString().split('T')[0]);
      
      
      setEndDate(today.toISOString().split('T')[0]);
  }
  const generateTableBody = () => {
    if (!data || !data[0] || !data[0].donnees_energie) {
      return null;
    }
  
    const transposedData = data.map((inverter) =>
      inverter.donnees_energie.map((data) => ({
        puissance: data.puissance,
        temps: formatDate(data.temps),
      }))
    );
  
    const countValues = {}; 
    const updateCount = (value, columnIndex) => {
      if (!countValues[columnIndex]) {
        countValues[columnIndex] = {};
      }
  
      if (!countValues[columnIndex][value]) {
        countValues[columnIndex][value] = 1;
      } else {
        countValues[columnIndex][value] += 1;
      }
    };
  
    return (
      <tbody id="tableau">
        {transposedData[0].map((_, rowIndex) => (
          <tr key={rowIndex}>
            <td id="tab_h" onClick={(e) => click_on_line(e, rowIndex)}>
              {formatDate(data[0].donnees_energie[rowIndex].temps)}
            </td>
            <td id="tab_h"> {data[0].donnees_energie[rowIndex].irradiance_en_watt_par_surface}</td>
  
            {transposedData.map((row, cellIndex) => {
              const value = row && row[rowIndex] ? parseInt(row[rowIndex].puissance) : '';
  
              updateCount(value, cellIndex);
              const isBelowCounter = value <= compteur;
  
              const isRed = countValues[cellIndex] && countValues[cellIndex][value] >= 3;
  
              return (
                <td
                  key={cellIndex + 3}
                  id="tab_h"
                  onClick={(e) => click_on_line(e, rowIndex, cellIndex)}
                  className={`tab_h ${
                    isBelowCounter ? 'zero-value' : ''
                  } ${
                    clickedRows.some(
                      (item) => item.rowIndex === rowIndex && item.celll - 2 === cellIndex
                    )
                      ? 'clicked-row'
                      : ''
                  } ${isRed ? 'zero-value' : ''}`}
                  onContextMenu={(e) => handleContextMenu(e, rowIndex, cellIndex)}
                >
                  {value}
                </td>
              );
            })}
          </tr>
        ))}
      </tbody>
    );
  };
  
    return(
     <div>
      <select id='filtre_centrale' onChange={changement_centrale}>
        {data_cate.map((item) =>(<option id="selec_centrale">{item.nomCentrale}</option>))}
      </select>
      <p id="para_dispo">Dispo Albioma: {valeurDispo}</p>


      <div id="compteur">
        <p>Seuil: {compteur} W</p>
        <div id="boutons_compteurs">
          <button onClick={incrementer}>+</button>
          <button onClick={decrementer}>-</button>
        </div>
      </div>

      <div id="select-period">
        <label>Période:</label>
        <select value={selectedPeriod} onChange={(e) => handlePeriodChange(e)}>
          <option value="1 semaine">1 semaine</option>
          <option value="2 semaines">2 semaines</option>
          <option value="1 mois">1 mois</option>
          <option value="autre">Autre</option>
        </select>
      </div>

      <div><input
      id="checkbox_show"
          type="checkbox"
          checked={isChecked}
          onChange={handleCheckboxChange}/></div>

    <div id="tab_container">
      
      <table id="tab_cate">
          {generateTableHeader()}
          {generateTableBody()}
      </table>
      
      
      {menuVisible && (
        <div
          className="menu-contextuel"
          style={{ top: positionMenu.top, left: positionMenu.left }}
        >
          <table id="body">
            <thead id="head_cate">
              <th>
                Catégorisation Erreur
              </th>
              <th></th>
            </thead>
            <tbody id="body_css">
              {donnees.map((ligne, index) => (
              <tr key={index} >
                <td  id="body">{ligne.texte}</td>
                <td id="body">
                  <button onClick={() => ouvrir_overlay_2(index)}>{ligne.boutonTexte}</button>
                </td>
              </tr>
            ))}
              </tbody>
          </table>
          <button id="button_close_overlay_1" onClick={close_overlay_1}>Annuler</button>
        </div>
      )}


       {secondOverlayVisible && (
        <div className="second-overlay" style={{ top: secondOverlayPosition.top, left: secondOverlayPosition.left }}>

          <form method="post" action="traitement.php">
            <p id="text_inside">
              <label for="ameliorer">Commentaires</label><br />
              <textarea name="ameliorer" id="ameliorer"></textarea>
            </p>
          </form>
          <div>
            <button id="confirm_cate" onClick={(index) => envoi_categorisation('confirmer')}>Confirmer</button>
            <button id="cancel_cate" onClick={(index) => envoi_categorisation('annuler')}>Annuler</button>
          </div>
        </div>
      )}

      
        </div>
        {showCalendarOverlay && (
        <div id="calendar-overlay" style={{ top: periodSelectorPosition.top-10, left: periodSelectorPosition.left-10 }}>
          <div id="frame">
            <button id="button_close_calendar" onClick={close_calendar}>&lt;</button>
            <div>
            <div>
              <label style={{color:'black'}}>Date de début: </label>
              <input
                type="date"
                value={startDate || ''}
                onChange={(e) => handleDateSelect(new Date(e.target.value))}
              />
            </div>

            <div>
              <label style={{color:'black'}}>Date de fin: </label>
              <input
                type="date"
                value={endDate || ''}
                onChange={(e) => handleEndDateSelect(new Date(e.target.value))}
              />
            </div>

            <div>
              <Calendar onSelectDate={handleDateSelect} />
            </div>
            </div>
          
          </div>
          </div>
          )}
      </div>
    );
}