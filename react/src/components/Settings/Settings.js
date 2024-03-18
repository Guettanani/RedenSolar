import React from 'react';

import EditUser from '../Component/EditUser';
import GrappeEdit from '../Component/GrappeEdit';

const Settings = () => {

  return (
    <div className="container-fluid p-3">
      {/* Titre */}
      <h2 className='text-center'>Paramètres</h2>
      <hr />

      {/* Composant permettant de modifier les utilisateurs */}
      <EditUser />
      <hr />

      {/* Composant permettant de gérer les grappes */}
      <GrappeEdit/>
      <hr />

      {/* Lien vers l'administrateur django */}
      <div className='container-fluid p-3'>
        <div className='d-flex flex-column justify-content-center align-items-center rounded bg-dark p-4 gap-1'>
          <div className="">
            <h3 className="display-6 text-light text-center">Admin</h3>
            <a href={`https://webicamapp.reden.cloud/admin`} className="textset4" target="_blank">
              Accès à la modification des centrales et équipements
            </a>
            <hr />
          </div>
          {/* Reste du code pour la partie Admin */}
        </div>
      </div>



    </div>

  );
};

export default Settings;
