import { combineReducers } from 'redux';
import { reducer as formReducer } from 'redux-form';

import authReducer from './authReducer';
import fileReducer from './fileReducer';

export default combineReducers({
    auth : authReducer,
    form : formReducer,
    files : fileReducer
});
