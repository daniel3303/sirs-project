import sirs from "../apis/sirs";

import{
    USER_LOGIN,
    USER_LOGIN_FAILED,
    USER_LOGIN_SUCCESS,
    USER_LOGOUT,
    USER_REGISTER,
    USER_REGISTER_SUCCESS,
    USER_REGISTER_FAILED,
    FETCH_FILES,
    FETCH_FILE,
    UPDATE_FILE,
    CREATE_FILE
}  from "./types";

export const login = (username, password) => async (dispatch, getState) => {
    dispatch({ type: USER_LOGIN });
    const response = await sirs.post('/users', { username, password });

    if(response.data.status === "success"){
        dispatch({ type: USER_LOGIN_SUCCESS, payload: { username, password, name: response.data.name, userId: response.data.userId, loggedFromRegister: false } });
    }else{
        dispatch({ type: USER_LOGIN_FAILED });
    }

};

export const register = (name, username, password) => async (dispatch, getState) => {
    dispatch({ type: USER_REGISTER });
    const {data} = await sirs.post('/users/create', { name, username, password });

    if(data.status === "success"){
        dispatch({ type: USER_REGISTER_SUCCESS });
        dispatch({ type: USER_LOGIN_SUCCESS, payload: { userId: data.userId, username, password, name: data.name, loggedFromRegister: true} });
    }else{
        dispatch({ type: USER_REGISTER_FAILED, payload: data.message });
    }

};

export const logout = () => {
    return {
        type: USER_LOGOUT
    };
};

export const fetchFiles = () => async (dispatch, getState) => {
    const response = await sirs.get('/files', {params: { username: getState().auth.username, password: getState().auth.password }});

    dispatch({
            type: FETCH_FILES,
            payload: response.data.files
    });
};


export const fetchFile = (id) => async (dispatch, getState) => {
    const response = await sirs.get(`/files/${id}`, {params: { username: getState().auth.username, password: getState().auth.password }});

    dispatch({
            type: FETCH_FILE,
            payload: response.data.file
    });
};

export const updateFile = (id, newValues) => async (dispatch, getState) => {
    const response = await sirs.post(`/files/${id}`, {...newValues, username: getState().auth.username, password: getState().auth.password });

    dispatch({
        type: UPDATE_FILE
    });
    dispatch(fetchFile(id));
};


export const createFile = (values) => async (dispatch, getState) => {
    const response = await sirs.post("/files/create", {...values, username: getState().auth.username, password: getState().auth.password });

    dispatch({
        type: CREATE_FILE
    })

    dispatch(fetchFile(response.data.file.id));
}
