import React from 'react';
import ReactDOM from 'react-dom';
import { connect } from 'react-redux';
import { BrowserRouter, Route, Switch, Redirect } from 'react-router-dom';


import FilesList from './files/FilesList';
import FileEdit from './files/FileEdit';
import Login from './Login.js';
import Register from './Register.js';
import Header from './Header';

class App extends React.Component {
    constructor(props){
            super(props);

    };

    componentDidMount = () => {
        //this.state
    }

    renderLoggedOutRoutes = () => {
        return (
            <React.Fragment>
                <Route path="/register" exact component={Register}/>
                <Route path="/login" exact component={Login}/>
                <Route path="/" exact component={Login}/>
            </React.Fragment>
        );
    }

    renderLoggedInRoutes = () => {
        return (
            <React.Fragment>
                <Route path="/files/:id" exact component={FileEdit} />
                <Route path="/files" exact component={FilesList}/>
                <Route path="/" exact component={() => <Redirect to="/files" />}/>
            </React.Fragment>
        );
    }

    render() {
        return (
            <BrowserRouter>
                <div>
                    <Header />
                    <Switch>
                        { (this.props.isLoggedIn) ? this.renderLoggedInRoutes() : this.renderLoggedOutRoutes() }
                    </Switch>
                </div>
            </BrowserRouter>
        );
    };
}

const mapStateToProps = state => {
    return { isLoggedIn: state.auth.isLoggedIn };
}

export default connect(mapStateToProps)(App);
