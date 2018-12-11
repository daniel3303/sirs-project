import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';

import { fetchFiles } from '../../actions';
import FileCreate from './FileCreate';

class FilesList extends React.Component {
    interval = null;
    componentDidMount() {
        this.props.fetchFiles();
        this.interval = setInterval(() => {
            this.props.fetchFiles()
        }, 2000);
    }

    componentWillUnmount() {
        clearInterval(this.interval);
    }

    renderList(){
        if(this.props.files.length == 0){
            return <div>You have no files!</div>;
        }

        return this.props.files.map(file => {
            return (
                <div className="item" key={file.id}>
                    <i className="large middle aligned icon file" />
                    <div className="content">
                        <Link to={`/app/files/${file.id}`} className="header">
                            {file.name}
                        </Link>
                        <div className="description">
                            Permissions: {(file.permissions.read) ? "r" : ""}{(file.permissions.write) ? "w" : ""}
                            { (file.owner === this.props.userId) ? <div>You own this file</div> : <div>You DO NOT own this file</div> }
                            { (file.corrupted === true) ? <div className="ui orange header" style={{fontSize: "1em"}}>This file is corrupted</div> : "" }
                        </div>
                    </div>
                </div>
            );
        });
    }

    render() {
            return (
                <div className="ui grid centered">
                    <div className="seven wide column">
                        <div className="ui huge header">List of files {(this.props.files.length > 0) ? "("+this.props.files.length+")" : ""}</div>
                        <div className="ui celled list">{this.renderList()}</div>
                    </div>
                    <div className="five wide column">
                        <FileCreate />
                    </div>
                </div>
        );
    }
}

const mapStateToProps = state => {
    return {
        userId: state.auth.userId,
        files: Object.values(state.files),
        userId: state.auth.userId,
        isLoggedIn: state.auth.isLoggedIn
    };
};

export default connect(
    mapStateToProps,
    { fetchFiles }
)(FilesList);
