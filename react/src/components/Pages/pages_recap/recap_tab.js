import React from 'react';
import './recap_tab.css';
export default function TabRecap() {

    

    return(
        <div>

        <div id='container_tab_recap'>
            <table id='tabrecap'>
                <thead >
                    <th id="cellrecap">Mois</th>
                    <th id="cellrecap">Jan.</th>
                    <th id="cellrecap">Fév.</th>
                    <th id="cellrecap">Mars</th>
                    <th id="cellrecap">Avril</th>
                    <th id="cellrecap">Mai</th>
                    <th id="cellrecap">Juin</th>
                    <th id="cellrecap">Juillet</th>
                    <th id="cellrecap">Août</th>
                    <th id="cellrecap">Sep.</th>
                    <th id="cellrecap">Oct.</th>
                    <th id="cellrecap">Nov.</th>
                    <th id="cellrecap">Dec.</th>
                </thead>
                <tbody>
                  
                    <tr><td id="cellrecap_2">Production Réelle</td></tr>
                    <tr><td id="cellrecap_2">Production Attendue</td></tr>
                    <tr><td id="cellrecap_2">Performance Ratio Réelle</td></tr>
                    <tr><td id="cellrecap_2">Performance Ratio Brute</td></tr>
                    <tr><td id="cellrecap_2">Production Ratio attendu</td></tr>
                    <tr><td id="cellrecap_2">Disponibilité Brute</td></tr>
                    <tr><td id="cellrecap_2">Disponibilité Reden</td></tr>
                    <tr><td id="cellrecap_2">Disponibilité Contractuelle</td></tr>
                    
                </tbody>
            </table>
        </div>
        </div>
    );
}