import { useState } from 'react';
import Navbar from './components/Navbar'
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Helmet } from 'react-helmet';



import logo from './components/Assets/REDEN_logo.png'
// import {FaTable} from 'react-icons/fa'
import {IoReorderThreeOutline} from 'react-icons/io5'
import LoginSignup from './components/LoginSignup/LoginSignup';
import ResetPassword from './components/LoginSignup/ResetPassword/ResetPassword';
import Settings from './components/Settings/Settings';
import Categories from "./components/Pages/categories";
import Recap from "./components/Pages/recapitulatif";
import MC from "./components/Pages/main_courante";
import TableauDispo from  "./components/Pages/Tableau";
//import Categories from './components/components/Pages/Categories';

function App() {
  // const [showNav, setShowNav] = useState(false);
  

  return (
    
    <div className="App">
      <Helmet>
        <title>Reden</title>
        <meta name="description" content="Description de votre page" />
        <link rel="icon" type="image/png" href={logo} />
      </Helmet>
      
      <header>
        {/* <IoReorderThreeOutline onClick={() => setShowNav(!showNav)} /> */}
        <img src={logo} alt='Logo' className='logo' />
        <Navbar />
      </header>
      
      <div className="main">
        <Routes>
          <Route path="/" element={<LoginSignup />} />
          <Route path="/ResetPassword" element={<ResetPassword />} />
          <Route path="/Settings" element={<Settings />} />
          <Route path="/recapitulatif" element={<Recap/>} />
          <Route path="/categories" element={<Categories/>} />
          <Route path="/main_courante" element={<MC/>} />
          <Route path="/recap_tab" element={<TableauDispo/>} />
        </Routes>
      </div>
    </div> 
  );
}

export default App;
