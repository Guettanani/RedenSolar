import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../../App.css';


const Tableau = ({ SelectCentrale, start, end, Leseuil, setClickedData, setShowModal, onlyError }) => {
    const [data, setData] = useState([]);
    const [clickedRows, setClickedRows] = useState([]);
    const [AlreadyCategoriseData, setAlreadyCategoriseData] = useState([]);
    const [onlyErrorData, setonlyErrorData] = useState([]);
    const [loading, setLoading] = useState(false);

    const fetchdatacentrale = async () => {
        try {
            setData([]);
            setLoading(true); // Définir l'état de chargement sur true au début de la requête

            if (start || end) {
                const response = await axios.get("http://localhost:8050/getCentrale/", {
                    params: {
                        selected_nom: SelectCentrale ? SelectCentrale : 'Abattoirs de Langogne',
                        date_debut: start,
                        date_fin: end
                    }
                });

                const responseData = response.data;
                // responseData.forEach((item) => {
                //     if (item.donnees_energie && item.donnees_energie.length > 0) {
                //         item.donnees_energie.sort((a, b) => {
                //             const tempsA = new Date(a.temps);
                //             const tempsB = new Date(b.temps);
                //             return tempsA.getTime() - tempsB.getTime();
                //         });
                //     } else {
                //         console.error(`donnees_energie is undefined or empty for item with idReferenceOnduleur: ${item.idReferenceOnduleur}`);
                //     }
                // });
                if (responseData.some(item => item.donnees_energie && item.donnees_energie.length > 0)) {
                    setData(responseData);
                } else {
                    setData([]);
                }

                setLoading(false); // Définir l'état de chargement sur false une fois que les données sont récupérées
                console.log("ResponseAPI" + JSON.stringify(responseData));
                console.log("Data :" + JSON.stringify(data));
            }
        } catch (error) {
            console.error("Une erreur s'est produite : ", error);
            setLoading(false); // Assurez-vous également de désactiver le chargement en cas d'erreur
        }
    };

    const CalculErrorData = () => {
        const listErrorData = [];

        // Vérifier si data est défini et n'est pas vide
        if (data && data.length > 0) {
            data.forEach(aOnduleurData => {
                // Vérifier si aOnduleurData et aOnduleurData.donnees_energie sont définis et ne sont pas vides
                if (aOnduleurData && aOnduleurData.donnees_energie && aOnduleurData.donnees_energie.length > 0) {
                    aOnduleurData.donnees_energie.forEach((adata, index) => {
                        const AlreadyCategorise = CheckCategoriseData(aOnduleurData.nomReference, adata);
                        if (adata && adata.puissance && adata.temps && adata.puissance <= Leseuil && !AlreadyCategorise) {
                            listErrorData.push({
                                nomReference: aOnduleurData.nomReference,
                                puissance: adata.puissance,
                                temps: adata.temps,
                                rowIndex: index
                            });
                        }
                    });
                }
            });
        }

        setonlyErrorData(listErrorData);
        console.log("error : " + JSON.stringify(onlyErrorData));
    };

    useEffect(() => {
        CalculErrorData();
    }, [Leseuil, data]);

    useEffect(() => {
        fetchdatacentrale();
    }, [start, end, SelectCentrale]);

    useEffect(() => {
        // InitData();
        fetchdatacentrale();
        // generateAlreadyCategoriseData();
        CalculErrorData();
    }, []);


    useEffect(() => {
        setClickedData(clickedRows);
    }, [clickedRows]);

    const handleContextMenu = (e) => {
        e.preventDefault();
        setShowModal(true);
    };
    //Vérifier si l'élémment est deja catégorise
    const CheckCategoriseData = (EquipementData, data) => {
        return AlreadyCategoriseData.some((item) =>
            item.nomReference === EquipementData
            && item.puissance === data.puissance
            && item.temps === data.temps
        )
    }


    const click_on_line = (e, rowIndex, cellIndex) => {
        const nomReference = data[cellIndex].nomReference ? data[cellIndex].nomReference : "";
        const temps = data[cellIndex].donnees_energie[rowIndex].temps ? data[cellIndex].donnees_energie[rowIndex].temps : "";
        const puissance = data[cellIndex].donnees_energie[rowIndex].puissance ? data[cellIndex].donnees_energie[rowIndex].puissance : "";

        const DataClick = {
            rowIndex,
            cellIndex,
            puissance,
            nomReference,
            temps
        }
        // Vérifier si DataClick est déjà dans clickedRows
        const isAlreadyClicked = clickedRows.some(item => (
            item.rowIndex === DataClick.rowIndex &&
            item.cellIndex === DataClick.cellIndex &&
            item.puissance === DataClick.puissance &&
            item.nomReference === DataClick.nomReference &&
            item.temps === DataClick.temps
        ));

        const AlreadyCategorise = CheckCategoriseData(DataClick.nomReference, DataClick);

        //Verification des touches de manipulation des données
        const isCtrlPressed = e.ctrlKey || e.metaKey;
        const isShiftPressed = e.shiftKey;

        // Si DataClick n'est pas déjà dans clickedRows, l'ajouter
        if (!isAlreadyClicked && isCtrlPressed && puissance <= Leseuil && !AlreadyCategorise) {
            const newClickedRows = [...clickedRows, DataClick];
            setClickedRows(newClickedRows);
        } else if (!isAlreadyClicked && isShiftPressed && puissance <= Leseuil && !AlreadyCategorise) {
            const [startRow, startCol] = [clickedRows[0].rowIndex, clickedRows[0].cellIndex];
            const [endRow, endCol] = [rowIndex, cellIndex];

            // Determine selection direction and iterate over cells:
            const isSelectingDown = endRow >= startRow;
            const isSelectingRight = endCol >= startCol;

            const updatedClickedRows = clickedRows.slice(); // Create a copy to avoid mutation

            for (let i = startRow; isSelectingDown ? i <= endRow : i >= endRow; i += isSelectingDown ? 1 : -1) {
                for (let j = startCol; isSelectingRight ? j <= endCol : j >= endCol; j += isSelectingRight ? 1 : -1) {
                    const cellData = {
                        rowIndex: i,
                        cellIndex: j,
                        puissance: data[j].donnees_energie[i].puissance,
                        nomReference: data[j].nomReference, // Assuming Onduleur data is accessible based on cell index
                        temps: data[j].donnees_energie[i].temps, // Assuming DateTime is accessible within data structure
                    };

                    if (!updatedClickedRows.some(item => (
                        item.rowIndex === cellData.rowIndex &&
                        item.cellIndex === cellData.cellIndex &&
                        item.puissance === DataClick.puissance &&
                        item.nomReference === cellData.nomReference &&
                        item.temps === cellData.temps
                    )) && cellData.puissance <= Leseuil && !AlreadyCategoriseData.some((item) =>
                        item.nomReference === cellData.nomReference
                        && item.puissance === cellData.puissance
                        && item.temps === cellData.temps
                    )) {
                        updatedClickedRows.push(cellData);
                    }
                }
            }

            setClickedRows(updatedClickedRows);
        } else if (puissance <= Leseuil && !AlreadyCategorise) {
            setClickedRows([DataClick]);
        }

        console.log("Row Clicked : " + JSON.stringify(clickedRows));

    }

    const generateTableBody = () => {

        if (!data || data.some(item => !item.donnees_energie)) {
            return <h2 className='text-center display-2'>Aucunes données pour cette période avec cette centrale</h2>;
        }

        return (
            <tbody id="tableau" className='table-group-divider'>
                {data.findIndex(item => item.donnees_energie) !== -1 && ( // Check if index found
                    data[data.findIndex(item => item.donnees_energie)].donnees_energie.map(
                        (rowdata, rowIndex) => (
                            (onlyError && !onlyErrorData.some(RowToShow => RowToShow.rowIndex === rowIndex))
                                ? null
                                :
                                <tr key={rowIndex}>
                                    <td
                                        id={"tab_heure_" + data[data.findIndex(item => item.donnees_energie)].donnees_energie[rowIndex].temps}
                                        className='table-primary'
                                        onMouseDown={(e) => e.preventDefault()}
                                    // onClick={(e) => click_on_line(e, rowIndex)}
                                    >
                                        {/* {formatDate(data[0].donnees_energie[rowIndex].temps)} */}
                                        {data[data.findIndex(item => item.donnees_energie)].donnees_energie[rowIndex].temps}
                                    </td>
                                    <td
                                        id={"tab_irradiance_" + data[data.findIndex(item => item.donnees_energie)].donnees_energie[rowIndex].temps}
                                        className='border-irradiance'
                                        onMouseDown={(e) => e.preventDefault()}
                                    >
                                        {data[data.findIndex(item => item.donnees_energie)].donnees_energie[rowIndex].irradiance_en_watt_par_surface}
                                    </td>
                                    {data.map((row, cellIndex) => {
                                        const rowData = row.donnees_energie[rowIndex];
                                        const value = rowData ? rowData.puissance ?? '' : ''; // Utilisation de l'opérateur de coalescence nulle
                                        return (
                                            <td
                                                key={cellIndex + 3}
                                                id={"tab_" + cellIndex + "_" + rowIndex}
                                                onClick={(e) => click_on_line(e, rowIndex, cellIndex)}
                                                onMouseDown={(e) => e.preventDefault()}
                                                className={
                                                    `${(clickedRows.some(
                                                        (item) => item.rowIndex === rowIndex && item.cellIndex === cellIndex
                                                    ))
                                                        ? 'table-info-perso'
                                                        : (AlreadyCategoriseData.length > 0 && AlreadyCategoriseData.some((item) =>
                                                            item.nomReference === row.nomReference
                                                            // && item.puissance === (rowData ? rowData.puissance : null)
                                                            && item.temps === (rowData ? rowData.temps : null)))
                                                            ? 'table-success-perso'
                                                            : (onlyErrorData.length > 0 && onlyErrorData.some((item) =>
                                                                item.nomReference === row.nomReference
                                                                // && item.puissance === (rowData ? rowData.puissance : null)
                                                                && item.temps === (rowData ? rowData.temps : null)))
                                                                ? 'table-danger-perso'
                                                                : 'table-secondary-perso'
                                                    }
            `}
                                                onContextMenu={(e) => handleContextMenu(e, rowIndex, cellIndex)}
                                            >
                                                {value}
                                            </td>
                                        );
                                    })}
                                </tr>
                        )))}
            </tbody>
        );
    };

    const generateTableHeader = () => {
        return (
            <thead className="sticky-perso">
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

    return (
        <div className='col-12 overflow-x-scroll'>
            {loading ? (
                // Afficher le spinner Bootstrap si loading est true
                <div className='d-flex flex-column justify-content-center align-items-center col-12'>
                    <div className="spinner-border text-primary" role="status">
                    </div>
                    <span className="sr-only">Chargement des données...</span>
                </div>
            ) : (
                // Afficher la table si loading est false
                <table id="tab_cate" className='table table-hover text-center table-responsive'>
                    {generateTableHeader()}
                    {generateTableBody()}
                </table>
            )}
        </div>
    );

};

export default Tableau;
