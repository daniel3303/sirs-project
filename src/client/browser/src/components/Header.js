import React from 'react';
import { Link } from 'react-router-dom';
import UserHeaderMenu from './UserHeaderMenu';

const Header = () => {
  return (
    <div className="ui secondary pointing menu" style={{backgroundColor:"#cacaca"}}>
        <div className="item" style={{display:"flex", alignItems:"center", height:"100%"}}>
            <Link to="/" style={{fontSize: "24px", color:"black"}}>
                SIRS@A47
            </Link>
        </div>

        <div className="right menu">
            <UserHeaderMenu />
        </div>
    </div>
  );
};

export default Header;
