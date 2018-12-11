import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import { fetchFile, updateFile, createRole, checkFileChanged } from '../../actions';
import FileForm from './FileForm';
import FileRolesForm from './FileRolesForm';
import FileRolesList from './FileRolesList';



class FileEdit extends React.Component{
    interval = null;


    componentWillMount(){
        this.props.fetchFile(this.props.match.params.id);
        this.startFileMonitoring();
    }

    startFileMonitoring = () => {
        if(this.interval == null){
            this.interval = setInterval(() => {
                this.props.checkFileChanged(this.props.match.params.id);
            }, 2000);
        }
    }

    stopFileMonitoring = () =>{
        if(this.interval != null){
            clearInterval(this.interval);
            this.interval = null;
        }
    }




    componentWillUnmount() {
        clearInterval(this.interval);
    }

    onFileFormSubmit = (formValues) => {
        this.props.updateFile(this.props.match.params.id, formValues);
        this.stopFileMonitoring();
        setTimeout(this.startFileMonitoring, 2000); //Not so good
    }

    onFileRoleFormSubmit = (formValues) => {
        this.props.createRole(this.props.match.params.id, formValues);
    }

    refetchFile = () => {
        this.props.fetchFile(this.props.match.params.id);
    }

    renderFileChanged(){
        if(this.props.fileChanged && !this.props.file.corrupted){
            return (
                <div className="ui red message">
                    <div className="header" style={{textAlign:"center"}}>
                        <p>Seems like this file was updated by someone else.</p>
                        <button className="ui button" onClick={this.refetchFile}>
                            <i className="sync icon"></i> Reload file
                        </button>
                    </div>
                </div>
            );
        }
        return "";
    }

    renderFileCorrupted(){
        if(this.props.corrupted){
            return (
                <div className="ui red message">
                    <div className="header" style={{textAlign:"center"}}>
                        <p>This file is corrupted and because of that the content may have been changed.<br />
                        Your changes will override the corrupted file.
                        </p>
                    </div>
                </div>
            );
        }
        return "";
    }


    render(){
        if(!this.props.file){
            return <div>Loading...</div>;
        }

        return (
            <div className="ui grid centered">
                <div className="seven wide column">
                    {this.renderFileCorrupted()}
                    {this.renderFileChanged()}
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
    return {
        file : state.files[ownProps.match.params.id],
        userId: state.auth.userId, fileChanged:
        state.files[ownProps.match.params.id].changed,
        corrupted: state.files[ownProps.match.params.id].corrupted
    };
}

export default connect(mapStateToProps, {fetchFile, updateFile, createRole, checkFileChanged})(FileEdit);
