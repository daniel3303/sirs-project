import React from 'react';
import { connect } from 'react-redux';
import { Field, reduxForm } from 'redux-form';
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


    render(){
        return (
            <form onSubmit={this.props.handleSubmit(this.onSubmit)} className="ui form error">
                <Field name="username" component={this.renderInput} label="Username" />
                <Field name="password" component={this.renderInput} label="Password" />
                <button className="ui button primary">Login</button>
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

export default connect(null, { login })(reduxForm({
    form: 'loginForm',
    validate
})(Login));
