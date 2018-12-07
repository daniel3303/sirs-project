import React from 'react';
import "./LoginForm.css";


class LoginForm extends React.Component{
    constructor(props){
        super(props);
        this.state = {

        }
    }


    render = () => {
        return (
            <div className="login-form">
                <div className="ui middle center centered aligned three column grid">
                    <div className="row">
                        <div className="column">
                            <div className="ui vertical fluid menu">
                                <div className="header item">
                                    <div className="ui field large icon input">
                                        <input type="text" placeholder="Utilizador" />
                                        <i className="user icon"></i>
                                    </div>
                                    <div className="ui field large icon input">
                                        <input type="text" placeholder="Password" />
                                        <i className="lock icon"></i>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}


export default LoginForm;
