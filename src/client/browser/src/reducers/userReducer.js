import _ from 'lodash';

import {
    FETCH_USERS
} from '../actions/types';

export default (state = {}, action) => {
    switch (action.type) {
        case FETCH_USERS:

            return { ...state, ..._.mapKeys(action.payload, 'id') };
    }

    return state;
};
