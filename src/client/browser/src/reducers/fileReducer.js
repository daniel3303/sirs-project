import _ from 'lodash';

import {
    FETCH_FILES,
    FETCH_FILE,
    UPDATE_FILE,
    CREATE_FILE,
    CREATE_ROLE,
    FETCH_ROLES,
} from '../actions/types';

export default (state = {}, action) => {
    switch (action.type) {
    case FETCH_FILES:
        return _.merge({}, state, _.mapKeys(action.payload, 'id'));
    case FETCH_FILE:
        console.log(action);
        return _.merge({}, state, {[action.payload.id]: action.payload});
    case UPDATE_FILE:
        return { ...state };
    case CREATE_FILE:
        return { ...state };
    case CREATE_ROLE:
        return { ...state };
    case FETCH_ROLES:
        return _.merge({}, state, {[action.payload.fileId]: action.payload});
    default:
        return state;
    }
};
