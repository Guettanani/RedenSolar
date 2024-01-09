import React from 'react';
import './Navbar.css';
import { Link } from 'react-router-dom';

const Navbar = ({ show }) => {
    const close = () => {
        show && show(false);
    }

    return (
        <div className={show ? 'sidenav active' : 'sidenav'}>
            <ul>
                <li>
                    <Link to="/categories" onClick={close}>
                        Catégorisation
                    </Link>
                </li>
            </ul>
            <ul>
                <li>
                    <Link to="/recapitulatif" onClick={close}>
                        Récapitulatif
                    </Link>
                    <Link to="/recap_tab" onClick={close}>
                        Tableau
                    </Link>
                    <a >Diagramme</a>
                    <a >Graphique</a>
                </li>
            </ul>
            <ul>
                <li>
                    <Link to="/main_courante" onClick={close}>
                        Main Courante
                    </Link>
                </li>
            </ul>
            <ul>
                <li>
                    <Link to="/Settings" onClick={close}>
                        Paramètres
                    </Link>
                </li>
            </ul>
            <ul>
                <li>
                    <Link to="/" onClick={close}>
                        Déconnexion
                    </Link>
                </li>
            </ul>
        </div>
    );
}

export default Navbar;