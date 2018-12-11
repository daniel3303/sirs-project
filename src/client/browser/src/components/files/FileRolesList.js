import React from 'react'
import { connect } from 'react-redux';

import { fetchRoles, revokeRole } from '../../actions';

class FileRolesList extends React.Component{
    componentDidMount = () => {
        this.props.fetchRoles(this.props.fileId);
    }

    onRevokeClick = (userId) => {
        this.props.revokeRole(this.props.fileId, userId);
    }

    renderRoles = () => {
        if(this.props.roles.length == 0){
            return <div>This file has no roles assign to it.</div>;
        }

        return this.props.roles.map((role, index) => {
            return (
                <div className="item" key={index}>
                    <div className="right floated content">
                        <div className="ui button" onClick={() => {this.onRevokeClick(role.user.id)}}>Revoke</div>
                    </div>
                    <img className="ui avatar image" src="/app/avatar.png" />
                    <div className="content">
                        <span className="header">{role.user.username} ({role.user.name})</span>
                        Permissions:  {(role.read) ? "read " : ""}{(role.write) ? "write" : ""}
                    </div>
                </div>
            );
        });
    }

    render = () => {
        if(this.props.file.owner != this.props.userId){
            return <div>You can´t see the roles for this file because you don't own it.</div>
        }

        if(!this.props.file.roles){
            return (<div>Loading...</div>);
        }

        return (
            <div className="ui middle aligned divided list">
                { this.renderRoles() }
            </div>
        );

    }

}


const mapStateToProps = (state, ownProps) =>{
    return {
            file: state.files[ownProps.fileId],
            roles: state.files[ownProps.fileId].roles,
            userId: state.auth.userId
    };
}


export default connect(mapStateToProps, { fetchRoles, revokeRole })(FileRolesList);
