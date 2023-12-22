import React from 'react';
import './ResetPassword.css';
import { Link } from 'react-router-dom';

import email_icon from '../../Assets/email.png';
// import REDEN_logo from 'C:/Users/loris/OneDrive/Documents/GitHub/reden-solar/src/components/Assets/REDEN_logo.png';

const ResetPassword = () => {
  return (
    <div className="page">
      {/* Frame or Header */} 
     <div className="header-frame">
        {/* Add your frame/header content here */}
        {/* <img src={REDEN_logo} alt="" style={{ width: '180px', height: 'auto' }}/>
        <h1> </h1>
        <h1>|</h1>
        <h1> </h1>
        <h1>Logiciel pour le calcul de disponibilités des centrales</h1>
        {/* img src={REDEN_logo} alt="" You can add any other elements like navigation links or icons here */}
      </div>

      {/* Main Content */}
      <div className='container'>
        <div className="header">
          <div className="text">Récupération de mot de passe</div>
          <div className="underline"></div>
        </div>
        <div className="inputs">
          <div className="input">
            <img src={email_icon} alt="" />
            <input type="email" placeholder='Adresse email' />
          </div>
        </div>
        <div className="forgot-password">Veuillez entrer votre adresse email pour retrouver votre compte.</div>

        <div className="submit-container">
          <div className="submit"> <Link to="/">Retour</Link></div>
          <div className="submit">Envoyer</div>
        </div>
      </div>
    </div>
  );
};

export default ResetPassword;
//Veuillez entrer votre adresse email pour retrouver votre compte//
