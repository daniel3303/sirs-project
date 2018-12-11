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
                <Route path="/app/register" exact component={Register}/>
                <Route path="/app/login" exact component={Login}/>
                <Route path="/app/" exact component={Login}/>
                <Route path="/app/index.html" exact component={() => <Redirect to="/app/" />}/>
            </React.Fragment>
        );
    }

    renderLoggedInRoutes = () => {
        return (
            <React.Fragment>
                <Route path="/app/files/:id" exact component={FileEdit} />
                <Route path="/app/files" exact component={FilesList}/>
                <Route path="/app/" exact component={() => <Redirect to="/app/files" />}/>
                <Route path="/app/index.html" exact component={() => <Redirect to="/app/" />}/>
            </React.Fragment>
        );
    }

    render() {
        return (
            <BrowserRouter>
                <React.Fragment>
                    <Header />
                    <Switch>
                        { (this.props.isLoggedIn) ? this.renderLoggedInRoutes() : this.renderLoggedOutRoutes() }
                    </Switch>
                </React.Fragment>
            </BrowserRouter>
        );
    };
}

const mapStateToProps = state => {
    return { isLoggedIn: state.auth.isLoggedIn };
}

export default connect(mapStateToProps)(App);
