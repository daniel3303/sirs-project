import React from 'react';
import { Link } from 'react-router-dom';
import UserHeaderMenu from './UserHeaderMenu';

const Header = () => {
  return (
    <div className="ui secondary pointing menu">
      <Link to="/" className="item">
        SIRS@A47
      </Link>
      <div className="right menu">
          <UserHeaderMenu />
      </div>
    </div>
  );
};

export default Header;
