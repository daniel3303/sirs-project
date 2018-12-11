import {
    USER_LOGIN,
    USER_LOGOUT,
    USER_LOGIN_FAILED,
    USER_LOGIN_SUCCESS,
    USER_REGISTER,
    USER_REGISTER_SUCCESS,
    USER_REGISTER_FAILED,
} from '../actions/types';

const INITIAL_STATE = {
    checkingRegister: false,
    registeredSuccess: null,
    loggedFromRegister: false,
    registerFailedMessage: "",

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
                        loggedFromRegister: action.payload.loggedFromRegister,
                        checkingLogin: false,
                        triedLogin: true
                     };
        case USER_LOGIN_FAILED:
            return { ...state,
                        checkingLogin: false,
                        triedLogin: true
            };
        case USER_LOGOUT:
            return { ...INITIAL_STATE };

        case USER_REGISTER:
            return { ...state, checkingRegister: true };

        case USER_REGISTER_SUCCESS:
            return { ...state, checkingRegister: false, registeredSuccess: true }

        case USER_REGISTER_FAILED:
            return { ...state, registerFailedMessage: action.payload, checkingRegister: false }

        default:
            return state;
    }
}
