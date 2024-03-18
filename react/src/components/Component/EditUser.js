import React, { useState } from 'react';

import user_icon from '../Assets/person.png';
// import email_icon from '../Assets/email.png';
// import password_icon from '../Assets/password.png';

const EditUser = () => {
    // Définition des états pour les champs de l'utilisateur
    const [showModal, setShowModal] = useState(false);
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [accessRights, setAccessRights] = useState('');

    const handleSave = () => {
        // Logique de sauvegarde de l'utilisateur
        const userData = {
            username: username,
            email: email,
            password: password
        };
        saveUser(userData);
        closeModal();
    };

    const closeModal = () => {
        setShowModal(false);
    };

    const saveUser = (userData) => {
        // Logique de sauvegarde de l'utilisateur
        console.log("Utilisateur sauvegardé :", userData);
        // Ajoutez votre logique de sauvegarde ici
    };

    const handleEditUser = () => {
        setShowModal(true);
    };

    return (
        <div className="container-fluid p-3">
            <div className='d-flex flex-column justify-content-center align-items-center rounded bg-dark p-4 gap-1 text-light'>
                <div className="">
                    <h3 className="display-6">User</h3>
                    <hr />
                </div>
                <div className="p-2 d-flex flex-column justify-content-center align-items-center">
                    <div className="input mb-3 p-2 col-12 gap-3 py-4">
                        <img src={user_icon} alt="" className="me-2" />
                        <div className="floating-label">
                            <label>Nom d'utilisateur</label>
                            <select className="form-select mb-3">
                                <option value="" disabled selected>Sélectionnez un utilisateur</option>
                                <option value="Benoit Dufour">Benoit Dufour</option>
                                <option value="John Doe">John Doe</option>
                                {/* Autres options... */}
                            </select>
                        </div>
                        <button className="btn btn-primary" onClick={handleEditUser}>Modifier</button>
                    </div>
                </div>
            </div>

            {/* Modal */}
            <div className={`modal fade ${showModal ? 'show d-block' : ''}`} tabIndex="-1" role="dialog">
                <div className="modal-dialog modal-dialog-centered" role="document">
                    <div className="modal-content">
                        <div className="modal-header">
                            <h5 className="modal-title">Modifier un utilisateur</h5>
                            <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close" onClick={closeModal}></button>
                        </div>
                        <div className="modal-body">
                            <div className="d-flex flex-column justify-content-center align-items-center gap-3">
                                <div className="p-2 col-12">
                                    <label htmlFor="Username">Nom d'utilisateur:</label>
                                    <input id="Username" className="form-control" placeholder="Benoit" value={username} onChange={(e) => setUsername(e.target.value)} />
                                </div>
                                <div className="p-2 col-12">
                                    <label htmlFor="email">Email:</label>
                                    <input id="email" type="email" className="form-control" placeholder="benoit@gmail.com" value={email} onChange={(e) => setEmail(e.target.value)} />
                                </div>
                                <div className="p-2 col-12">
                                    <label htmlFor="accessRights">Droit d'accès:</label>
                                    <select id="accessRights" className="form-select" value={accessRights} onChange={(e) => setAccessRights(e.target.value)}>
                                        <option value="">Sélectionnez un droit d'accès</option>
                                        <option value="Lecture">Lecture</option>
                                        <option value="Écriture">Écriture</option>
                                        <option value="Modification">Modification</option>
                                        {/* Ajoutez d'autres options au besoin */}
                                    </select>
                                </div>
                                <div className="p-2 col-12">
                                    <label htmlFor="password">Mot de passe:</label>
                                    <input id="password" type="password" className="form-control" placeholder="......" value={password} onChange={(e) => setPassword(e.target.value)} />
                                </div>
                            </div>
                        </div>
                        <div className="modal-footer">
                            <button type="button" className="btn btn-secondary" onClick={closeModal}>Annuler</button>
                            <button type="button" className="btn btn-primary" onClick={handleSave}>Valider</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default EditUser;
