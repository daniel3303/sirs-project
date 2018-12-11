import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';

class UserHeaderMenu extends React.Component{

    onLogoutClick = () =>{
        alert("Logout!!!");
    }

    render = () => {
        if(this.props.isLoggedIn){
            return (
                <div>
                    Welcome {this.props.name} 
                    <button className="ui button" onClick={this.onLogoutClick}>
                        Logout
                    </button>
                </div>
            );
        }else{
            return (
                <div>
                    <Link to="/login">Login</Link> |
                    <Link to="/register">Register</Link>
                </div>
            );
        }
    }


}


const mapStateToProps = (state, ownProps) => {
        return { isLoggedIn: state.auth.isLoggedIn, name: state.auth.name };
}

export default connect(mapStateToProps, {})(UserHeaderMenu);
