import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = ({ show }) => {
    const close = () => {
        show && show(false);
    }

    return (
        <div className={show ? 'sidenav active' : 'sidenav'}>
            <ul className="nav flex-column">
                <li className="nav-item my-2">
                    <Link to="/categories" className="nav-link mx-2" onClick={close}>
                        Catégorisation
                    </Link>
                </li>
                {/* <li className="nav-item my-2">
                    <Link to="/recapitulatif" className="nav-link mx-2" onClick={close}>
                        Récapitulatif
                    </Link></li> */}
                <li className="nav-item my-2">
                    <Link to="/recap_tab" className="nav-link mx-2" onClick={close}>
                        Tableau
                    </Link></li>
                {/* <li className="nav-item my-2">
                    <a href="#" className="nav-link mx-2" onClick={close}>Diagramme</a></li> */}
                {/* <li className="nav-item my-2">
                    <a href="#" className="nav-link mx-2" onClick={close}>Graphique</a>
                </li> */}
                <li className="nav-item my-2">
                    <Link to="/main_courante" className="nav-link mx-2" onClick={close}>
                        Main Courante
                    </Link>
                </li>
                <li className="nav-item my-2">
                    <Link to="/Settings" className="nav-link mx-2" onClick={close}>
                        Paramètres
                    </Link>
                </li>
                <li className="nav-item my-2">
                    <Link to="/" className="nav-link mx-2" onClick={close}>
                        Déconnexion
                    </Link>
                </li>
            </ul>
        </div>
    );
}

export default Navbar;