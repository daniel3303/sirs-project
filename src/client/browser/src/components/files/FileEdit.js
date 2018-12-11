import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import { fetchFile, updateFile, createRole } from '../../actions';
import FileForm from './FileForm';
import FileRolesForm from './FileRolesForm';
import FileRolesList from './FileRolesList';



class FileEdit extends React.Component{
    componentWillMount(){
        this.props.fetchFile(this.props.match.params.id);
    }

    onFileFormSubmit = (formValues) => {
        this.props.updateFile(this.props.match.params.id, formValues);
    }

    onFileRoleFormSubmit = (formValues) => {
        this.props.createRole(this.props.match.params.id, formValues);
    }

    render(){
        if(!this.props.file){
            return <div>Loading...</div>;
        }

        return (
            <div>
                <FileForm initialValues={{name: this.props.file.name, content: this.props.file.content}} onSubmit={this.onFileFormSubmit}/>
                <FileRolesList fileId={this.props.file.id}/>
                { (this.props.userId === this.props.file.owner) ?
                    <FileRolesForm onSubmit={this.onFileRoleFormSubmit}/>
                :
                    <div>You can't change permissions for this file because you don´t own it.</div>
                }
                <Link to={'/'} className="header">Return to list of files</Link>
            </div>
        );
    }


}

const mapStateToProps = (state, ownProps) => {
    return {file : state.files[ownProps.match.params.id], userId: state.auth.userId };
}

export default connect(mapStateToProps, {fetchFile, updateFile, createRole})(FileEdit);
