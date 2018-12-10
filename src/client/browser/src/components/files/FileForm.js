import React from 'react';
import { Field, reduxForm } from 'redux-form';


class FileForm extends React.Component{
    renderError({ error, touched }) {
        if (touched && error) {
            return (
                <div className="ui error message">
                    <div className="header">{error}</div>
                </div>
            );
        }
    }

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

    onSubmit = formValues => {
        this.props.onSubmit(formValues);
    };

    render() {
        return (
            <form
                onSubmit={this.props.handleSubmit(this.onSubmit)}
                className="ui form error"
            >
                <Field name="name" component={this.renderInput} label="File's name" />
                <Field name="content" component={this.renderInput} label="File's content" />
                <button className="ui button primary">Save</button>
            </form>
        );
    }
}

const validate = formValues => {
    const errors = {};

    if (!formValues.name) {
        errors.title = 'You must enter a file name';
    }

    if (!formValues.content && formValues.content != "") {
        errors.description = 'You must enter a description';
    }

    return errors;
}


export default reduxForm({
    form: 'fileForm',
    validate
})(FileForm);
