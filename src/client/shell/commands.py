import json
from sys import stderr
from urllib.parse import urljoin
from os import path, makedirs

LIST_FILES_RESOURCE = 'files'
CREATE_FILE_RESOURCE = 'files/create'
FILE_RESOURCE = 'files/%d'
ROLES_RESOURCE = 'files/%d/roles'
LIST_USERS = 'users'
REGISTER_USER_RESOURCE = 'users/create'

STRINGS_TRUE = ['True', 'T', 'TRUE', 'true']

DEFAULT_DOWNLOAD_FOLDER = path.abspath('downloads')


def _read(urlbase, sess, params):
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

    return file


def read(urlbase, sess, params):
    file = _read(urlbase, sess, params)
    if file is None:
        return

    numbered = params.get('numbered', 'False')

    print('Id:', file['id'])
    print('Name:', file['name'])
    print('Owner Id:', file['owner'])

    content = file['content']

    if not content:
        print('FILE IS EMPTY')
        return

    print('Content:')

    if numbered not in STRINGS_TRUE:
        print(content)
        return

    lines = content.split('\n')

    for idx, l in enumerate(lines):
        print(idx + 1, l, sep=': ')


def write(urlbase, sess, params):
    if params.get('content', None) is None:
        print('Argument "content" expected for command append')
        return

    if params.get('after', None) is None:
        print('Argument "after" expected for command append')
        return

    file = _read(urlbase, sess, params)
    if file is None:
        return

    filecontent = file['content']
    lines = filecontent.split('\n')

    content = params['content']
    after = int(params['after'])

    lines.insert(after, content)
    params['content'] = '\n'.join(lines)

    success = _change(urlbase, sess, params)

    if success:
        print('Content written with success')


def replace(urlbase, sess, params):
    if params.get('content', None) is None:
        print('Argument "content" expected for command append')
        return

    if params.get('line', None) is None:
        print('Argument "line" expected for command append')
        return

    file = _read(urlbase, sess, params)
    if file is None:
        return

    filecontent = file['content']
    lines = filecontent.split('\n')

    content = params['content']
    nline = int(params['line'])

    lines[nline - 1] = content
    params['content'] = '\n'.join(lines)

    success = _change(urlbase, sess, params)

    if success:
        print('Content replaced with success')


def erase(urlbase, sess, params):
    if params.get('line', None) is None:
        print('Argument "line" expected for command append')
        return

    file = _read(urlbase, sess, params)
    if file is None:
        return

    filecontent = file['content']
    lines = filecontent.split('\n')

    nline = int(params['line'])

    lines.pop(nline - 1)
    params['content'] = '\n'.join(lines)

    success = _change(urlbase, sess, params)

    if success:
        print('Content erased with success')


def append(urlbase, sess, params):
    if params.get('content', None) is None:
        print('Argument "content" expected for command append')
        return

    file = _read(urlbase, sess, params)
    if file is None:
        return

    content = params['content']

    params['content'] = '\n'.join([file['content'], content])

    success = _change(urlbase, sess, params)

    if success:
        print('Content appended with success')


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

    res = sess.post(url, data=reqjson)
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
    file = _read(urlbase, sess, params)
    if file is None:
        return

    location = params.get('location', DEFAULT_DOWNLOAD_FOLDER)
    name = params.get('file', file['name'])

    filename = path.join(location, name)

    makedirs(path.dirname(filename), exist_ok=True)

    if path.exists(filename):
        print('The file %s already exists' % filename)
        return

    with open(filename, 'w+') as pfile:
        pfile.write(file['content'])

    print('File downloaded')
    print('Saved at %s' % filename)


def ls(urlbase, sess, params):
    url = urljoin(urlbase, LIST_FILES_RESOURCE)

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

    files = resjson['files']
    if len(files) == 0:
        print('You don\'t have access to any file')
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

    res = sess.get(url, params=reqparams)
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

    changejson = json.dumps({
        'userId': params['userId'],
        'read': rd in STRINGS_TRUE,
        'write': wt in STRINGS_TRUE,
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

    res = sess.get(url)
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

def check_credentials_validity(urlbase, sess, params):
    if 'username' not in params:
        print('Argument "username" expected for command Check Credentials Validity')
        return

    if 'password' not in params:
        print('Argument "password" expected for command Check Credentials Validity')
        return False

    req = {
        'username': params['username'],
        'password': params['password']
    }

    url = urljoin(urlbase, LIST_USERS)
    reqjson = json.dumps(req)

    res = sess.post(url, data=reqjson)

    if res.status_code != 200:
        print('There was a problem during the request (status', res.status_code, ')', file=stderr)
        return False

    resjson = res.json()

    if resjson['status'] != 'success':
        print(resjson['message'], file=stderr)
        return False

    print(resjson['message'])

    return True
