import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <div className="ui secondary pointing menu">
      <Link to="/" className="item">
        SIRS@A47
      </Link>
      <div className="right menu">
          Sair
      </div>
    </div>
  );
};

export default Header;
