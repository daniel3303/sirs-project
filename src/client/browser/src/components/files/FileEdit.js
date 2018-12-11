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
            <div className="ui grid centered">
                <div className="seven wide column">
                    <div className="ui huge header">Edit file: {this.props.file.name}</div>
                    <FileForm initialValues={{name: this.props.file.name, content: this.props.file.content}} onSubmit={this.onFileFormSubmit}/>
                    <br />
                    <Link to={'/'} className="header">
                    <button className="ui labeled icon button">
                        <i className="chevron left icon"></i>
                        Return to list of files
                    </button>
                    </Link>
                </div>
                <div className="five wide column">
                    <div className="ui huge header">Roles to this file</div>
                    <FileRolesList fileId={this.props.file.id}/>

                    <div className="ui huge header">Edit file roles</div>
                    { (this.props.userId === this.props.file.owner) ?
                        <FileRolesForm onSubmit={this.onFileRoleFormSubmit}/>
                    :
                        <div>You can't change permissions for this file because you don´t own it.</div>
                    }
                </div>
            </div>
        );
    }


}

const mapStateToProps = (state, ownProps) => {
    return {file : state.files[ownProps.match.params.id], userId: state.auth.userId };
}

export default connect(mapStateToProps, {fetchFile, updateFile, createRole})(FileEdit);
