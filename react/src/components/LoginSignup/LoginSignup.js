import React, { useState } from 'react';
import './LoginSignup.css';
import { Link } from 'react-router-dom';

import user_icon from '../Assets/person.png';
import email_icon from '../Assets/email.png';
import password_icon from '../Assets/password.png';
// import REDEN_logo from '../Assets/REDEN_logo.png';

const LoginSignup = () => {
  const [action, setAction] = useState("Créer un compte utilisateur");

  return (
    <div className="page">
      {/* Frame or Header */} 
      <div className="header-frame">
        {/* Add your frame/header content here */}
        {/*<img src={REDEN_logo} alt="" style={{ width: '180px', height: 'auto' }}/>
        <h1> </h1>
        <h1>|</h1>
        <h1> </h1>
        <h1>Logiciel pour le calcul de disponibilités des centrales</h1>
        {/* img src={REDEN_logo} alt="" You can add any other elements like navigation links or icons here */}
      </div>

      {/* Main Content */}
      <div className='container'>
        <div className="header">
          <div className="text">{action}</div>
          <div className="underline"></div>
        </div>
        <div className="inputs">
          {action === "Se connecter" ? <div></div> : <div className="input">
            <img src={user_icon} alt="" />
            <input type="text" placeholder='Prénom, Nom' />
          </div>}

          <div className="input">
            <img src={email_icon} alt="" />
            <input type="email" placeholder='Adresse email' />
          </div>
          <div className="input">
            <img src={password_icon} alt="" />
            <input type="password" placeholder='Mot de passe' />
          </div>
        </div>
        {action === "Créer un compte utilisateur" ? <div></div> : 
            <div className="go-forgot-password"> Mot de passe oublié ? <span className="link">
                <Link to="/ResetPassword">Cliquez ici !</Link>
            </span>
            </div>}

        <div className="submit-container">
          <div className={action === "Se connecter" ? "submit gray" : "submit"} onClick={() => { setAction("Créer un compte utilisateur") }}>Créer un compte</div>
          <div className={action === "Créer un compte utilisateur" ? "submit gray" : "submit"} onClick={() => { setAction("Se connecter") }}><Link to="/Categories">Se connecter</Link></div>
        </div>
      </div>
    </div>
  );
};

export default LoginSignup;
