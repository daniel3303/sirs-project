import json
from sys import stderr
from urllib.parse import urljoin

LIST_FILES_RESOURCE = 'files'
CREATE_FILE_RESOURCE = 'files/create'
FILE_RESOURCE = 'files/%d'
REGISTER_USER_RESOURCE = 'users/create'


# TODO:
# Check if they receive the right parameters
# Check the response status code

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


def _create(urlbase, sess, params):
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

    file = resjson['file']
    return int(file['id'])


def create(urlbase, sess, params):
    id = _create(urlbase,sess, params)
    if id is None:
        return
    name = params['name']
    print('File %s created with id %d' % (name, id))


def upload(urlbase, sess, params):
    filename = params['file']
    if filename is None:
        print('Argument "file" expected for command upload')
        return

    name = params['name']
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

    res = sess.get(url, params=reqparams)
    resjson = res.json()
    if resjson['status'] != 'success':
        print(resjson['message'], file=stderr)
        return

    file = resjson['file']
    if file['corrupted']:
        print('', file=stderr)
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

    resjson = res.json()
    if resjson['status'] != 'success':
        print(resjson['message'], file=stderr)
        return

    print('File deleted with success')

def test(urlbase, sess, params):
    print(urlbase)
    print(sess)
    print(params)

    with sess.get(urlbase) as r:
        print(r.status_code)
        print(r.encoding)
        print(r.text)
