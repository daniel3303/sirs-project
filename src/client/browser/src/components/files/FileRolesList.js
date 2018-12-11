import React from 'react'
import { connect } from 'react-redux';

import { fetchRoles } from '../../actions';

class FileRolesList extends React.Component{
    componentDidMount = () => {
        this.props.fetchRoles(this.props.fileId)
    }

    renderRoles = () => {
        return this.props.roles.map(role => {
            return (
                <div key={role.user.username}>
                    User: {role.user.username} ({role.user.name})<br />
                    Permissions:  {(role.read) ? "r" : ""}{(role.write) ? "w" : ""}<br />
                    <br />
                </div>
            );
        });
    }

    render = () => {
        if(this.props.file.userId != this.props.userId){
            return <div>You can´t see the roles for this file because you don't own it.</div>
        }

        if(!this.props.file.roles){
            return <div>Loading...</div>;
        }

        return (
            <div>
                <h4>Roles</h4>
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


export default connect(mapStateToProps, { fetchRoles })(FileRolesList);
