import React from 'react';
import { Link } from 'react-router-dom';
import { FaTable, FaListAlt, FaClipboardList, FaCog, FaSignOutAlt } from 'react-icons/fa';

const Navbar = () => {
    return (
        <div className="navbar-container d-flex justify-content-center align-items-center flex-row">
            <ul className="d-flex justify-content-center align-items-center flex-row gap-3 mx-4">
                <li className="navbar-nav">
                    <Link to="/categories" className="d-flex justify-content-center align-items-center flex-column gap-1">
                        <FaListAlt /> <span>Catégories</span>
                    </Link>
                </li>
                <li className="navbar-nav">
                    <Link to="/recapitulatif" className="d-flex justify-content-center align-items-center flex-column gap-1">
                        <FaClipboardList /> <span>Récapitulatif</span>
                    </Link>
                </li>
                <li className="navbar-nav">
                    <Link to="/recap_tab" className="d-flex justify-content-center align-items-center flex-column gap-1">
                        <FaTable /> <span>Tableau</span>
                    </Link>
                </li>
                <li className="navbar-nav">
                    <Link to="/main_courante" className="d-flex justify-content-center align-items-center flex-column gap-1">
                        <FaClipboardList /> <span>Main Courante</span>
                    </Link>
                </li>
                <li className="navbar-nav">
                    <Link to="/Settings" className="d-flex justify-content-center align-items-center flex-column gap-1">
                        <FaCog /> <span>Paramètres</span>
                    </Link>
                </li>
                <li className="navbar-nav">
                    <Link to="/" className="d-flex justify-content-center align-items-center flex-column gap-1">
                        <FaSignOutAlt /> <span>Déconnexion</span>
                    </Link>
                </li>
            </ul>
        </div>
    );
}

export default Navbar;
