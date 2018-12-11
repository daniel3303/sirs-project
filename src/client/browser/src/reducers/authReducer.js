import { USER_LOGIN, USER_LOGOUT, USER_LOGIN_FAILED, USER_LOGIN_SUCCESS } from '../actions/types';

const INITIAL_STATE = {
    checkingLogin: false,
    triedLogin: false,
    isLoggedIn: false,
    userId: null,
    username: "",
    password: "",
    name: ""
}

export default (state = INITIAL_STATE, action) => {
    switch (action.type) {
        case USER_LOGIN:
            return { ...state, checkingLogin: true  };
        case USER_LOGIN_SUCCESS:
            return { ...state,
                        isLoggedIn: true,
                        userId: action.payload.userId,
                        username: action.payload.username,
                        password: action.payload.password,
                        name: action.payload.name,
                        checkingLogin: false,
                        triedLogin: true
                     };
        case USER_LOGIN_FAILED:
            return { ...state,
                        checkingLogin: false,
                        triedLogin: true
            };
        case USER_LOGOUT:
            return { ...state,
                isLoggedIn: false,
                userId: null,
                username: "",
                name: "",
                checkingLogin: false,
                triedLogin: false

            };
        default:
            return state;
    }
}
