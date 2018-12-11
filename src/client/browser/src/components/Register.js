import React from 'react';
import { connect } from 'react-redux';
import { Field, reduxForm } from 'redux-form';
import { Link, Redirect } from 'react-router-dom';

import { register } from '../actions';



class Register extends React.Component{
    renderError({ error, touched }) {
        if (touched && error) {
            return (
                <div className="ui error message">
                    <div className="header">{error}</div>
                </div>
            );
        }
    }

    onSubmit = ({name, username, password}) => {
        this.props.register(name, username, password);
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
        if(this.props.checkingRegister === true){
            return <button className="ui button primary"><i className="notched circle loading icon button"></i> Creating your account...</button>
        }else{
            return <button className="ui button primary">Register</button>
        }
    }


    render(){
        if(this.props.registeredSuccess){
            return <Redirect to="/" />;
        }

        return (
            <form onSubmit={this.props.handleSubmit(this.onSubmit)} className="ui form error">
                <Field name="name" component={this.renderInput} label="Name" />
                <Field name="username" component={this.renderInput} label="Username" />
                <Field name="password" component={this.renderInput} label="Password" />
                { this.renderSubmitButton() }
                { (this.props.registerFailedMessage) ? (<p className="ui red header">{ this.props.registerFailedMessage }</p>) : ""}
                <Link to="/" className="header">Already have an account? Click here to login</Link>
            </form>

        );
    }
}

const validate = formValues => {
    const errors = {};

    if (!formValues.name) {
        errors.password = 'You must type in your name';
    }
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
        isLoggedIn: state.auth.isLoggedIn,
        registeredSuccess: state.auth.registeredSuccess,
        checkingRegister: state.auth.checkingRegister,
        registerFailedMessage: state.auth.registerFailedMessage,
    }
}

export default connect(mapStateToProps, { register })(reduxForm({
    form: 'registerForm',
    validate
})(Register));
