import React from 'react';
import './Settings.css';

import user_icon from '../Assets/person.png';
import email_icon from '../Assets/email.png';
import password_icon from '../Assets/password.png';

const Settings = () => {
  // Function to get the IP address of the client

  return (
    <div className="headerset1">
      <div className="textset1">Paramètres</div>
      <div className="underlineset1"></div>
      <div className='containerset'>
        <div className="headerset2">
          <div className="textset2">Général</div>
          <div className="underlineset2"></div>
        </div>
        <div className="inputsset">
          <div className="inputset">
            <img src={user_icon} alt="" />
            <div className="textset3">Changer de Prénom, Nom :</div>
            <input type="textset" placeholder='user name' />
            <button> Sauvegarder </button>
          </div>
          <div className="underlineset3"></div>

          <div className="inputset">
            <img src={email_icon} alt="" />
            <div className="textset3">Changer d'adresse email :</div>
            <input type="email" placeholder='user email' />
            <button> Sauvegarder </button>
          </div>
          <div className="underlineset3"></div>

          <div className="inputset">
            <img src={password_icon} alt="" />
            <div className="textset3">Changer de mot de passe :</div>
            <input type="password" placeholder='.........' />
            <button> Sauvegarder </button>
          </div>
          <div className="underlineset3"></div>

        </div>
        <div className="save">Sauvegarder</div>
      </div>
      <div className='containerset'>
        <div className="headerset2">
          <div className="textset2">Admin</div>
          <div className="underlineset2"></div>
        </div>
        <div className="inputsset">
          <div className="inputset">
            <div className="textset3">Gestion des droits : </div>
            <select>
              <option value="option1">Bertrand, Dupont</option>
              <option value="option2">Julian, Meroux</option>
              <option value="option3">Paul, Belleville</option>
            </select>
            <select>
              <option value="option1">Administrateur</option>
              <option value="option2">Modification</option>
              <option value="option3">Visualisation</option>
            </select>
            <button> Sauvegarder </button>
          </div>
          <div className="underlineset3"></div>

          {/* Updated links with dynamically generated IP address */}

          <div className="inputset">
            <div className="textset3">
              <p>Django admin (Ajout/Suppression onduleurs,centrales...):</p>
            </div>
            <a href={`https://webicamapp.reden.cloud/admin`} className="textset4" target="_blank">
              {`https://webicamapp.reden.cloud/admin`}
            </a>
          </div>
          <div className="underlineset3"></div>

          <div className="underlineset3"></div>
        </div>
        <div className="save">Sauvegarder</div>
      </div>
    </div>
  );
};

export default Settings;
