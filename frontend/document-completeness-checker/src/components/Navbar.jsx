import React from 'react';
import logo from '../assets/logo.svg'

const Navbar = () => {
    return(
        <nav className="navbar-brand">
            <div>
                <img src={logo} alt="logo"/>

            </div>
            <div>
                <h1>DCC</h1>
            </div>
        </nav>
            )
}

export default Navbar;