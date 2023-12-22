import React from 'react';
import './Navbar.css';
import { Link } from 'react-router-dom';

const Navbar = ({ show }) => {
    return (
        <div className={show ? 'sidenav active' : 'sidenav'}>
            <ul>
                <li><Link to="/categories">Catégorisation</Link>

                </li>
            </ul>
            <ul>
                <li><Link to="/recapitulatif">Récapitulatif</Link>
                <li><Link to="/recap_tab">Tableau</Link>
                <a href="/">Diagramme</a>
                <a href="/">Graphique</a></li>

                </li>
                
            </ul>
            <ul>
                <li><Link to="/main_courante">Main Courante</Link>

                </li>
            </ul>
            <ul>
                <li><Link to="/Settings">Paramètres</Link>

                </li>
            </ul>
            <ul>
                <li><Link to="/">Déconnexion</Link>

                </li>
            </ul>
        </div>
    )
}

export default Navbar