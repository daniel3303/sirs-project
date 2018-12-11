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
    CREATE_FILE,
    FETCH_USERS,
    CREATE_ROLE,
    FETCH_ROLES,
    REVOKE_ROLE,
    FILE_CHANGED
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
    const {data} = await sirs.get(`/files/${id}`, {params: { username: getState().auth.username, password: getState().auth.password }});

    if(data.status === "success"){
        dispatch({
                type: FETCH_FILE,
                payload: data.file
        });
    }
};

export const updateFile = (id, newValues) => async (dispatch, getState) => {
    const {data} = await sirs.post(`/files/${id}`, {...newValues, username: getState().auth.username, password: getState().auth.password });

    if(data.status === "success"){
        dispatch({
            type: UPDATE_FILE,
            payload: {...newValues, id}
        });
        dispatch(fetchFile(id));
    }


};


export const createFile = (values) => async (dispatch, getState) => {
    const response = await sirs.post("/files/create", {...values, username: getState().auth.username, password: getState().auth.password });

    dispatch({
        type: CREATE_FILE
    })

    dispatch(fetchFile(response.data.file.id));
}

export const fetchUsers = () => async (dispatch, getState) => {
    const response = await sirs.get('/users', {params: { username: getState().auth.username, password: getState().auth.password }});

    dispatch({
            type: FETCH_USERS,
            payload: response.data.users
    });
};

export const createRole = (fileId, values) => async (dispatch, getState) => {
    const response = await sirs.post(`/files/${fileId}/roles`, {...values, username: getState().auth.username, password: getState().auth.password });

    dispatch({
            type: CREATE_ROLE,
    });

    dispatch(fetchRoles(fileId));
}


export const fetchRoles = (fileId) => async (dispatch, getState) => {
    const {data} = await sirs.get(`/files/${fileId}/roles`, {params: { username: getState().auth.username, password: getState().auth.password }});

    dispatch({
        type: FETCH_ROLES,
        payload: {
            fileId,
            roles: data.roles
        }
    });

}

export const revokeRole = (fileId, userId) => async (dispatch, getState) => {
    var params = {
        username: getState().auth.username,
        password: getState().auth.password,
        userId,
        read: false,
        write: false
    }
    const {data} = await sirs.post(`/files/${fileId}/roles`, params);

    dispatch({
        type: REVOKE_ROLE,
        payload: {
            fileId
        }
    });

    dispatch(fetchRoles(fileId));

}

export const checkFileChanged = (id) => async (dispatch, getState) => {
    const {data} = await sirs.get(`/files/${id}`, {params: { username: getState().auth.username, password: getState().auth.password }});

    if(data.status === "success"){
        var localFile = getState().files[id];
        var changed = false;

        if(localFile.content != data.file.content || localFile.name != data.file.name){
            changed = true;
        }

        dispatch({
                type: FILE_CHANGED,
                payload: {
                    id,
                    changed
                }
        });
    }
}
