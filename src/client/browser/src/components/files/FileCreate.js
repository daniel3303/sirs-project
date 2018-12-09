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
                <h4>Create new file</h4>
                <FileForm  onSubmit={this.onSubmit}/>
            </div>
        );
    }


}

export default connect(null, {createFile})(FileCreate);
