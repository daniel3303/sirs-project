from urllib.parse import urljoin

UPLOAD_RESOURCE = ''
DOWNLOAD_RESOURCE = ''


def read(urlbase, sess, params):
    pass


def write(urlbase, sess, params):
    pass


def upload(urlbase, sess, params):
    if len(params) < 1:
        print('Argument "name" expected for command upload')
        return

    url = urljoin(urlbase, UPLOAD_RESOURCE)
    name = params[0]

    with open(name, 'r') as file:
        content = file.read()
        sess.post(url, data=content)


def download(urlbase, sess, params):
    if len(params) < 1:
        print('Argument "name" expected for command download')
        return

    url = urljoin(urlbase, DOWNLOAD_RESOURCE)
    name = params[0]

    with open(name, 'w') as file:
        r = sess.get(url)
        file.write(r.text)


def ls(urlbase, sess, params):
    with sess.get(urlbase) as r:
        print(r.status_code)
        print(r.encoding)
        print(r.text)
        # print(r.json())


def test(urlbase, sess, params):
    print(urlbase)
    print(sess)
    print(params)

