import React from 'react';
import { Field, reduxForm } from 'redux-form';
import { connect } from 'react-redux';

import { fetchUsers } from '../../actions';


class FileRolesForm extends React.Component{
    renderError({ error, touched }) {
        if (touched && error) {
            return (
                <div className="ui error message">
                    <div className="header">{error}</div>
                </div>
            );
        }
    }

    componentDidMount = () =>{
        this.props.fetchUsers();
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

    renderBooleanInput = ({ input, label, meta }) => {
        const className = `field ${meta.error && meta.touched ? 'error' : ''}`;
        return (
            <div className={className}>
                <label>{label}</label>
                <select {...input} autoComplete="off">
                    <option value="" disabled defaultValue>Select an option</option>
                    <option value="true">Yes</option>
                    <option value="false">No</option>
                </select>
                {this.renderError(meta)}
            </div>
        );
    };

    renderUserSelectInput = ({ input, label, meta }) => {
        const className = `field ${meta.error && meta.touched ? 'error' : ''}`;

        return (
            <div className={className}>
                <label>{label}</label>
                <select {...input} autoComplete="off">
                    { this.props.users.map((user) => {
                        return <option value={user.id} key={user.id}>{user.username} ({user.name})</option>
                    }) }
                </select>
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
                <Field name="userId" component={this.renderUserSelectInput} label="Target user" />
                <Field name="read" component={this.renderBooleanInput} label="Read permissions" />
                <Field name="write" component={this.renderBooleanInput} label="Write permissions" />
                <button className="ui button primary">Save</button>
            </form>
        );
    }
}

const validate = formValues => {
    const errors = {};

    if (!formValues.userId) {
        errors.title = 'You must enter a file name';
    }
    if (!formValues.read) {
        errors.read = 'You must select a value for the read permission';
    }
    if (!formValues.write) {
        errors.write = 'You must select a value for the write permission';
    }

    return errors;
}

const mapStateToProps = (state) => {
    return { users: Object.values(state.users) };
}


export default connect(mapStateToProps, {fetchUsers})(reduxForm({
    form: 'fileRolesForm',
    validate
})(FileRolesForm));
