//Fichier de gestion de l'url de fetch
let urlAPI;

if (window.location.href.includes("localhost")) {
  urlAPI = "http://localhost:8050/";
} else {
  urlAPI = "https://webicamapp.reden.cloud/";
}

export default urlAPI;
