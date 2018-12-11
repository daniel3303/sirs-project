import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import { createFile } from '../../actions';
import FileForm from './FileForm'



class FileCreate extends React.Component{
    onSubmit = (formValues) => {
        this.props.createFile(formValues);
    }

    render(){
        return (
            <div>
                <div className="ui huge header">Create a new file</div>
                <FileForm  onSubmit={this.onSubmit}/>
            </div>
        );
    }


}

export default connect(null, {createFile})(FileCreate);
