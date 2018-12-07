import json
from sys import stderr
from urllib.parse import urljoin

LIST_FILES_RESOURCE = 'files'
CREATE_FILE_RESOURCE = 'files/create'
FILE_RESOURCE = 'file/%d'
REGISTER_USER_RESOURCE = 'users/create'


def read(urlbase, sess, params):
    pass


def write(urlbase, sess, params):
    pass


def register_user(urlbase, sess, params):
    if len(params) < 3:
        print('Arguments "username", "password and "name" expected for command Register User')
        return

    req = {
        'username': params['username'],
        'password': params['password'],
        'name': params['name']
    }

    url = urljoin(urlbase, REGISTER_USER_RESOURCE)
    reqjson = json.dumps(req)

    with sess.post(url, data=reqjson) as res:
        resjosn = res.json()
        if resjosn['status'] != 'success':
            print(resjosn['message'], file=stderr)
            return

    print('User created with success')


def create(urlbase, sess, params):
    if len(params) < 1:
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
    resjson = res.json()

    if resjson['status'] != 'success':
        print(resjson['message'], file=stderr)
        return

    print('File created with success')


def upload(urlbase, sess, params):
    if len(params) < 2:
        print('Arguments "name" and "file" expected for command upload')
        return

    createurl = urljoin(urlbase, CREATE_FILE_RESOURCE)
    name = params['name']
    file = params['file']

    createjson = json.dumps({'name': name})
    res = sess.post(createurl, data=createjson)
    resjson = res.json()

    if resjson['status'] != 'success':
        print(resjson['message'], file=stderr)
        return

    fileid = resjson['id']

    print('File created with success')

    change(urlbase, sess, {'id': fileid, 'file': file})


def change(urlbase, sess, params):
    if params.get('id', None) is not None:
        print('Arguments "id" expected for command change')
        return

    fileid = params['id']
    fileurl = urljoin(urlbase, FILE_RESOURCE % fileid)

    req = {}

    name = params.get('name', None)
    if name is not None:
        req['name'] = name

    file = params.get('file', None)
    if file is not None:
        with open(file, 'r') as pfile:
            req['content'] = pfile.read()

    changejson = json.dumps(req)
    res = sess.post(fileurl, data=changejson)

    resjson = res.json()
    if resjson['status'] != 'success':
        print(resjson['message'], file=stderr)
        return

    print('File updated with success')


def download(urlbase, sess, params):
    if len(params) < 2:
        print('Arguments "name" and "id" expected for command download')
        return

    fileid = int(params['id'])

    url = urljoin(urlbase, FILE_RESOURCE % fileid)
    reqparams = {
        'username': sess.auth[0],
        'password': sess.auth[1],
    }

    name = params['name']

    with open(name, 'w') as pfile:
        res = sess.get(url, params=reqparams)
        resjson = res.json()
        if resjson['status'] != 'success':
            print(resjson['message'], file=stderr)
            return

        file = resjson['file']
        if file['corrupted']:
            print('', file=stderr)
            return

        pfile.write(file['content'])


def ls(urlbase, sess, params):
    url = urljoin(urlbase, LIST_FILES_RESOURCE)

    reqparams = {
        'username': sess.auth[0],
        'password': sess.auth[1],
    }

    with sess.get(url, params=reqparams) as res:
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


def test(urlbase, sess, params):
    print(urlbase)
    print(sess)
    print(params)

    with sess.get(urlbase) as r:
        print(r.status_code)
        print(r.encoding)
        print(r.text)
