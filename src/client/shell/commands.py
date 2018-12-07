import json
from sys import stderr
from urllib.parse import urljoin

LIST_FILES_RESOURCE = 'files'
CREATE_FILE_RESOURCE = 'files/create'
FILE_RESOURCE = 'files/%d'
ROLES_RESOURCE = 'files/%d/roles'
LIST_USERS = 'users'
REGISTER_USER_RESOURCE = 'users/create'


def read(urlbase, sess, params):
    if params.get('id', None) is None:
        print('Argument "id" expected for command download')
        return

    fileid = int(params['id'])

    url = urljoin(urlbase, FILE_RESOURCE % fileid)
    reqparams = {
        'username': sess.auth[0],
        'password': sess.auth[1],
    }

    res = sess.get(url, params=reqparams)

    if res.status_code != 200:
        print('There was a problem during the request (status', res.status_code, ')', file=stderr)
        return

    resjson = res.json()
    if resjson['status'] != 'success':
        print(resjson['message'], file=stderr)
        return

    file = resjson['file']
    if file['corrupted']:
        print('The file is corrupted', file=stderr)
        return

    print('Id:', file['id'])
    print('Name:', file['name'])
    print('Owner Id:', file['owner'])
    print('Content:')
    print('  ', file['content'])


def write(urlbase, sess, params):
    pass  # TODO


def register_user(urlbase, sess, params):
    if params.get('username', None) is None:
        print('Arguments "username" expected for command Register User')
        return

    if params.get('password', None) is None:
        print('Arguments "password expected for command Register User')
        return

    if params.get('name', None) is None:
        print('Argument "name" expected for command Register User')
        return

    req = {
        'username': params['username'],
        'password': params['password'],
        'name': params['name']
    }

    url = urljoin(urlbase, REGISTER_USER_RESOURCE)
    reqjson = json.dumps(req)

    with sess.post(url, data=reqjson) as res:
        if res.status_code != 200:
            print('There was a problem during the request (status', res.status_code, ')', file=stderr)
            return

        resjosn = res.json()

        if resjosn['status'] != 'success':
            print(resjosn['message'], file=stderr)
            return

    print('User created with success')


def _create(urlbase, sess, params):
    if params.get('name', None) is None:
        print('Argument "name" expected for command upload')
        return

    createurl = urljoin(urlbase, CREATE_FILE_RESOURCE)
    name = params['name']

    createjson = json.dumps({
        'name': name,
        'username': sess.auth[0],
        'password': sess.auth[1],
    })
    res = sess.post(createurl, data=createjson)

    if res.status_code != 200:
        print('There was a problem during the request (status', res.status_code, ')', file=stderr)
        return

    resjson = res.json()

    if resjson['status'] != 'success':
        print(resjson['message'], file=stderr)
        return

    file = resjson['file']
    return int(file['id'])


def create(urlbase, sess, params):
    id = _create(urlbase, sess, params)

    if id is None:
        return

    name = params['name']

    print('File %s created with id %d' % (name, id))


def upload(urlbase, sess, params):
    filename = params.get('file', None)
    if filename is None:
        print('Argument "file" expected for command upload')
        return

    name = params.get('name', None)
    if name is None:
        print('Argument "name" expected for command upload')
        return

    fileid = _create(urlbase, sess, params)
    params['id'] = str(fileid)

    with open(filename) as pfile:
        params['content'] = pfile.read()

    success = _change(urlbase, sess, params)
    if success:
        print('File %s upload with id %d' % (name, fileid))


def _change(urlbase, sess, params):
    if params.get('id', None) is None:
        print('Arguments "id" expected for command change')
        return False

    fileid = int(params['id'])
    fileurl = urljoin(urlbase, FILE_RESOURCE % fileid)

    req = {
        'username': sess.auth[0],
        'password': sess.auth[1],
    }

    name = params.get('name', None)
    if name is not None:
        req['name'] = name

    content = params.get('content', None)
    if content is not None:
        req['content'] = content

    changejson = json.dumps(req)
    res = sess.post(fileurl, data=changejson)

    if res.status_code != 200:
        print('There was a problem during the request (status', res.status_code, ')', file=stderr)
        return

    resjson = res.json()
    if resjson['status'] != 'success':
        print(resjson['message'], file=stderr)
        return False

    return True


def change(urlbase, sess, params):
    success = _change(urlbase, sess, params)

    if success:
        print('File updated with success')


def download(urlbase, sess, params):
    if params.get('id', None) is None:
        print('Argument "id" expected for command download')
        return

    if params.get('name', None) is None:
        print('Argument "name" expected for command download')
        return

    fileid = int(params['id'])

    url = urljoin(urlbase, FILE_RESOURCE % fileid)
    reqparams = {
        'username': sess.auth[0],
        'password': sess.auth[1],
    }

    name = params['name']

    res = sess.get(url, params=reqparams)

    if res.status_code != 200:
        print('There was a problem during the request (status', res.status_code, ')', file=stderr)
        return

    resjson = res.json()
    if resjson['status'] != 'success':
        print(resjson['message'], file=stderr)
        return

    file = resjson['file']
    if file['corrupted']:
        print('The file is corrupted', file=stderr)
        return

    with open(name, 'w+') as pfile:
        pfile.write(file['content'])

    print('File downloaded')


def ls(urlbase, sess, params):
    url = urljoin(urlbase, LIST_FILES_RESOURCE)

    reqparams = {
        'username': sess.auth[0],
        'password': sess.auth[1],
    }

    with sess.get(url, params=reqparams) as res:

        if res.status_code != 200:
            print('There was a problem during the request (status', res.status_code, ')', file=stderr)
            return

        resjson = res.json()

        if resjson['status'] != 'success':
            print(resjson['message'], file=stderr)
            return

        files = resjson['files']
        if len(files) == 0:
            print('You don\'t own any file')
            return

        print('id', 'name', 'owner id', 'corrupted', 'read permission', 'write permission', sep='|')
        for f in files:
            print(
                f['id'],
                f['name'],
                f['owner'],
                f['corrupted'],
                f['permissions']['read'],
                f['permissions']['write']
                , sep='|'
            )


def delete(urlbase, sess, params):
    if params.get('id', None) is None:
        print('Arguments "id" expected for command delete')
        return

    fileid = int(params['id'])
    fileurl = urljoin(urlbase, FILE_RESOURCE % fileid)

    req = {
        'username': sess.auth[0],
        'password': sess.auth[1],
    }

    deletejson = json.dumps(req)
    res = sess.delete(fileurl, data=deletejson)

    if res.status_code != 200:
        print('There was a problem during the request (status', res.status_code, ')', file=stderr)
        return

    resjson = res.json()
    if resjson['status'] != 'success':
        print(resjson['message'], file=stderr)
        return

    print('File deleted with success')


def check_permissions(urlbase, sess, params):
    if params.get('id', None) is None:
        print('Argument "id" expected for command Check Permissions')
        return

    fileid = int(params['id'])

    url = urljoin(urlbase, ROLES_RESOURCE % fileid)

    reqparams = {
        'username': sess.auth[0],
        'password': sess.auth[1],
    }

    with sess.get(url, params=reqparams) as res:
        if res.status_code != 200:
            print('There was a problem during the request (status', res.status_code, ')', file=stderr)
            return

        resjson = res.json()

        if resjson['status'] != 'success':
            print(resjson['message'], file=stderr)
            return

        roles = resjson['roles']
        if len(roles) == 0:
            print('You didn\'t gave permissions over this file to anyone')
            return

        print('id', 'username', 'name', 'read permission', 'write permission', sep='|')
        for r in roles:
            user = r['user']
            print(
                user['id'],
                user['username'],
                user['name'],
                r['read'],
                r['write'],
                sep='|'
            )


def manage_permissions(urlbase, sess, params):
    if params.get('fileId', None) is None:
        print('Argument "fileId" expected for command Manage Permissions')
        return

    if params.get('userId', None) is None:
        print('Argument "userId" expected for command Manage Permissions')
        return

    fileid = int(params['fileId'])
    fileurl = urljoin(urlbase, ROLES_RESOURCE % fileid)

    rd = params.get('read', 'False')
    wt = params.get('write', 'False')

    stringstrue = ['True', 'T', 'TRUE']
    changejson = json.dumps({
        'userId': params['userId'],
        'read': rd in stringstrue,
        'write': wt in stringstrue,
        'username': sess.auth[0],
        'password': sess.auth[1],
    })

    res = sess.post(fileurl, data=changejson)

    if res.status_code != 200:
        print('There was a problem during the request (status', res.status_code, ')', file=stderr)
        return

    resjson = res.json()
    if resjson['status'] != 'success':
        print(resjson['message'], file=stderr)
        return

    print('User permissions changed with success')


def list_users(urlbase, sess, params):
    url = urljoin(urlbase, LIST_USERS)

    with sess.get(url) as res:
        if res.status_code != 200:
            print('There was a problem during the request (status', res.status_code, ')', file=stderr)
            return

        resjson = res.json()

        if resjson['status'] != 'success':
            print(resjson['message'], file=stderr)
            return

        users = resjson['users']
        if len(users) == 0:
            print('There aren\'t any User registered in the system')
            return

        print('id', 'username', 'name', sep='|')
        for user in users:
            print(
                user['id'],
                user['username'],
                user['name'],
                sep='|'
            )


def test(urlbase, sess, params):
    print(urlbase)
    print(sess)
    print(params)

    with sess.get(urlbase) as r:
        print(r.status_code)
        print(r.encoding)
        print(r.text)
