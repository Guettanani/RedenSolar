import { useState } from 'react';
import Navbar from './components/Navbar'
import './App.css';
import {Routes, Route} from "react-router-dom"

import logo from './components/Assets/REDEN_logo.png'
// import {FaTable} from 'react-icons/fa'
import {IoReorderThreeOutline} from 'react-icons/io5'
import LoginSignup from './components/LoginSignup/LoginSignup';
import ResetPassword from './components/LoginSignup/ResetPassword/ResetPassword';
import Settings from './components/Settings/Settings';
import Categories from "./components/Pages/categories";
import Recap from "./components/Pages/recapitulatif";
import MC from "./components/Pages/main_courante";
import TabRecap from "./components/Pages/pages_recap/recap_tab";
//import Categories from './components/components/Pages/Categories';

function App() {
  const [ showNav, setShowNav ] = useState(false)
  return (
    <div className="App">
      <header> <IoReorderThreeOutline on onClick={() => setShowNav(!showNav)}/> <img src={logo} alt='Logo'
      className='logo' /></header>
      
      <Navbar show={showNav} />
      <div className="main">
        <Routes>
          <Route path="/" element={<LoginSignup />} onClick={() => setShowNav(!showNav)}/>
          <Route path="/recap_tab" element={<TabRecap/>} onClick={() => setShowNav(!showNav)}/>
          <Route path="/ResetPassword" element={<ResetPassword />} onClick={() => setShowNav(!showNav)}/>
          <Route path="/Settings" element={<Settings />} onClick={() => setShowNav(!showNav)}/>
          <Route path="/recapitulatif" element={<Recap/>} onClick={() => setShowNav(!showNav)}/>
          <Route path="/categories" element={<Categories/>} onClick={() => setShowNav(!showNav)}/>
          <Route path="/main_courante" element={<MC/>} onClick={() => setShowNav(!showNav)}/>
        </Routes>
      </div>
    </div> 
  );
}

export default App;
