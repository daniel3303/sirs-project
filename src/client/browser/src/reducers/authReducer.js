import { USER_LOGIN, USER_LOGOUT } from '../actions/types';

const INITIAL_STATE = {
    isLoggedIn: false,
    userId: null,
    username: "",
    password: "",
    name: ""
}

export default (state = INITIAL_STATE, action) => {
    switch (action.type) {
        case USER_LOGIN:
            return { ...state,
                "isLoggedIn": true,
                "userId": action.payload.userId,
                "username": action.payload.username,
                "password" : action.payload.password,
                "name": action.payload.name
            };
        case USER_LOGOUT:
            return { ...state,
                "isLoggedIn": false,
                "userId": null,
                "username": "",
                "name": ""
            };
        default:
            return state;
    }
}
