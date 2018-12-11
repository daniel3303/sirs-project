import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';

import { logout } from '../actions';

class UserHeaderMenu extends React.Component{

    onLogoutClick = () =>{
        this.props.logout();
    }

    render = () => {
        if(this.props.isLoggedIn){
            return (
                <div className="item" style={{display: "flex", alignItems: "center", height:"100%"}}>
                    <img className="ui mini circular image" src="/avatar.png" />
                    <div className="content" style={{marginLeft:"10px"}}>
                      <div className="ui sub header">{this.props.name}</div>
                      <span style={{cursor:"pointer"}} onClick={this.onLogoutClick}>Logout</span>
                    </div>
                </div>
            );
        }else{
            return (
                <div className="item" style={{display: "flex", alignItems: "center", height:"100%"}}>
                    <Link to="/">
                        <button className="ui secondary button">
                            <i className="icon users"></i>
                            Login
                        </button>
                    </Link>
                    <Link to="/register">
                        <button className="ui secondary button">
                        <i className="icon wpforms"></i>
                            Register
                        </button>
                    </Link>
                </div>
            );
        }
    }


}


const mapStateToProps = (state, ownProps) => {
        return { isLoggedIn: state.auth.isLoggedIn, name: state.auth.name };
}

export default connect(mapStateToProps, {logout})(UserHeaderMenu);
