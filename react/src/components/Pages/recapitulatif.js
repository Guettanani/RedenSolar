import React from 'react';
import './recapitulatif.css';
import {Link} from 'react-router-dom';
export default function Recap() {
    return(
        <div id='container'>
            <div id='recap_tableau'>
            <Link to="/recap_tab">
                <img src='/tab.jpg' alt='lien'/>
                </Link>
            </div>
            <Link id='recap_graphe' >
                <img src='/Graphe.jpg' alt='lien'/>
                </Link>
            <Link  id='recap_camembert'>   
                <img src='/Camembert.jpg' alt='lien'/>
                </Link>
        </div>
    );
}