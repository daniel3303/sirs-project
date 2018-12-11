import _ from 'lodash';

import {
    FETCH_FILES,
    FETCH_FILE,
    UPDATE_FILE,
    CREATE_FILE,
    CREATE_ROLE
} from '../actions/types';

export default (state = {}, action) => {
    switch (action.type) {
    case FETCH_FILES:
        return { ...state, ..._.mapKeys(action.payload, 'id') };
    case FETCH_FILE:
        return { ...state, [action.payload.id]: action.payload };
    case UPDATE_FILE:
        return { ...state };
    case CREATE_FILE:
        return { ...state };
    case CREATE_ROLE:
        return { ...state };
    default:
        return state;
    }
};
