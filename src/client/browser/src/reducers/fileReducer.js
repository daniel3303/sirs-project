import _ from 'lodash';

import {
    FETCH_FILES,
    FETCH_FILE,
    UPDATE_FILE,
    CREATE_FILE,
    CREATE_ROLE,
    FETCH_ROLES,
    REVOKE_ROLE,
    USER_LOGOUT,
    FILE_CHANGED,
} from '../actions/types';

export default (state = {}, action) => {
    switch (action.type) {
    case FETCH_FILES:
        return {..._.mapKeys(action.payload, 'id')};
    case FETCH_FILE:
        return _.merge({}, state, {[action.payload.id]: {...action.payload, changed: false}});
    case UPDATE_FILE:
        return _.merge({}, state, {[action.payload.id]: action.payload});
    case CREATE_FILE:
        return { ...state };
    case CREATE_ROLE:
        return { ...state };
    case FETCH_ROLES:
        var newState = {...state};
        newState[action.payload.fileId].roles = action.payload.roles
        return newState;
    case REVOKE_ROLE:
        return { ...state };
    case USER_LOGOUT:
        return {};
    case FILE_CHANGED:
        var newState = {...state};
        newState[action.payload.id].changed = action.payload.changed;
        newState[action.payload.id].corrupted = action.payload.corrupted;
        return newState;
    default:
        return state;
    }
};
