import React from 'react';
import ReactDOM from 'react-dom';
import LoginForm from './components/LoginForm';

class App extends React.Component {
    constructor(props){
            super(props);

    };

    componentDidMount = () => {
        //this.state
    }

    render() {
        return (
            <LoginForm />
        );
    };
}

export default App
