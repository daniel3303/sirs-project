import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';

import { fetchFiles } from '../../actions';
import FileCreate from './FileCreate';

class FilesList extends React.Component {
    componentDidMount() {
        this.props.fetchFiles();
    }

    renderList(){
        return this.props.files.map(file => {
            return (
                <div className="item" key={file.id}>
                    <i className="large middle aligned icon file" />
                    <div className="content">
                        <Link to={`/files/${file.id}`} className="header">
                            {file.name}
                        </Link>
                        <div className="description">Permissions: {(file.permissions.read) ? "r" : ""}{(file.permissions.write) ? "w" : ""}</div>
                    </div>
                </div>
            );
        });
    }

    render() {
            return (
            <div>
                <h2>Ficheiros</h2>
                <div className="ui celled list">{this.renderList()}</div>
                <FileCreate />
            </div>
        );
    }
}

const mapStateToProps = state => {
    return {
        files: Object.values(state.files),
        userId: state.auth.userId,
        isLoggedIn: state.auth.isLoggedIn
    };
};

export default connect(
    mapStateToProps,
    { fetchFiles }
)(FilesList);
