import React from 'react';
import { Link } from 'react-router-dom';
import { SlLayers } from "react-icons/sl";
import { GrDocumentPerformance } from "react-icons/gr";
import { AiOutlineSolution } from "react-icons/ai";
import { RiSettings3Line, RiLogoutBoxLine } from 'react-icons/ri';

const Navbar = () => {
    return (
        <div className="navbar-container d-flex justify-content-center align-items-center flex-row">
            <ul className="d-flex justify-content-center align-items-center flex-row mx-4">
                <li className="navbar-nav">
                    <Link to="/categories" className="d-flex justify-content-center align-items-center flex-column gap-1">
                        <SlLayers /><span>Catégories</span>
                    </Link>
                </li>
                <li className="navbar-nav">
                    <Link to="/recap_tab" className="d-flex justify-content-center align-items-center flex-column gap-1">
                        <GrDocumentPerformance /> <span>Récapitulatif</span>
                    </Link>
                </li>
                <li className="navbar-nav">
                    <Link to="/main_courante" className="d-flex justify-content-center align-items-center flex-column gap-1">
                        <AiOutlineSolution /><span>Main Courante</span>
                    </Link>
                </li>
                <li className="navbar-nav">
                    <Link to="/Settings" className="d-flex justify-content-center align-items-center flex-column gap-1">
                        <RiSettings3Line /> <span>Paramètres</span>
                    </Link>
                </li>
                <li className="navbar-nav">
                    <Link to="/" className="d-flex justify-content-center align-items-center flex-column gap-1">
                        <RiLogoutBoxLine /> <span>Déconnexion</span>
                    </Link>
                </li>
            </ul>
        </div>
    );
}

export default Navbar;
