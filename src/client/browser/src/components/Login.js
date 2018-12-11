import React from 'react';
import { connect } from 'react-redux';
import { Field, reduxForm } from 'redux-form';
import { Link } from 'react-router-dom';

import { login } from '../actions';



class Login extends React.Component{
    renderError({ error, touched }) {
        if (touched && error) {
            return (
                <div className="ui error message">
                    <div className="header">{error}</div>
                </div>
            );
        }
    }

    onSubmit = ({username, password}) => {
        this.props.login(username, password);
    };

    renderInput = ({ input, label, meta }) => {
        const className = `field ${meta.error && meta.touched ? 'error' : ''}`;
        return (
            <div className={className}>
                <label>{label}</label>
                <input {...input} autoComplete="off" />
                {this.renderError(meta)}
            </div>
        );
    };

    renderSubmitButton = () =>{
        if(this.props.checkingLogin === true){
            return <button className="ui button primary"><i className="notched circle loading icon button"></i> Checking credentials...</button>
        }else{
            return <button className="ui button primary">Login</button>
        }
    }


    render(){
        return (
            <form onSubmit={this.props.handleSubmit(this.onSubmit)} className="ui form error">
                <Field name="username" component={this.renderInput} label="Username" />
                <Field name="password" component={this.renderInput} label="Password" />
                { this.renderSubmitButton() }
                { (this.props.triedLogin && !this.props.isLoggedIn) ? (<p className="ui red header">Login failed!</p>) : ""}
                <Link to="/register" className="header">Don´t have an account? Click here to create one</Link>
            </form>

        );
    }
}

const validate = formValues => {
    const errors = {};

    if (!formValues.username) {
        errors.username = 'You must type in your username';
    }

    if (!formValues.password) {
        errors.password = 'You must type in your password';
    }

    return errors;
};

const mapStateToProps = (state, ownProps) => {
    return {
        triedLogin: state.auth.triedLogin,
        isLoggedIn: state.auth.isLoggedIn,
        checkingLogin: state.auth.checkingLogin
    }
}

export default connect(mapStateToProps, { login })(reduxForm({
    form: 'loginForm',
    validate
})(Login));
