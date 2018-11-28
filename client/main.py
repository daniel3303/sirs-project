import sys
import json
import requests
from client.commands import *


def loadconfig(filename):
    with open(filename) as file:
        content = file.read()

    config = json.loads(content)

    return config


option_has_value = {
    'u': True,
    'p': True,
    'c': True,
    'i': False
}


def getoptionvalue(opt, param):
    if len(param) != 0 and option_has_value.get(opt):
        return param.pop(0)


def getoptions(param):
    if len(param) == 0:
        return {}

    opt = param.pop(0)
    if opt[0] != '-':
        return getoptions(param)

    rs = {}

    idx = 0
    for idx in range(1, len(opt) - 1):
        if idx == 1 and opt[idx] == '-':
            break

        rs.setdefault(opt[idx])

    idx = idx + 1
    opt = opt[idx:]
    rs.setdefault(opt, getoptionvalue(opt, param))

    rrs = getoptions(param)

    return {**rs, **rrs}


def authenticate(opts):
    username = opts.get('u') or opts.get('username')
    password = opts.get('p') or opts.get('password')
    return username, password


def sessionconfig(sess, config, opts):
    cert = config['cert']
    sess.verify = cert
    sess.auth = authenticate(opts)


cmdprocessors = {
    'ls': ls,
    'test': test,
    'upload': upload,
    'download': download,
}


def process(url, sess, cmd, flags):
    processor = cmdprocessors.get(cmd)

    if processor is None:
        print('Invalid Command')
        return

    try:
        processor(url, sess, flags)
    except requests.exceptions.ConnectionError as ce:
        print(ce, file=sys.stderr)


def parsecmd(strcmd):
    cmd, *params = strcmd.split(' ')
    return cmd, params


def process_cmd(val, url, session):
    if val:
        cmd, params = parsecmd(val)
        process(url, session, cmd, params)
    else:
        print('Argument expected for the -c option ')


def interactive(url, session):
    while True:
        i = input('>>')
        cmd, flags = parsecmd(i)

        if cmd == 'exit':
            break

        if not cmd:
            continue

        process(url, session, cmd, flags)


def main(args):
    config = loadconfig('config.json')
    url = "%s:%d" % (config['address'], config['port'])

    with requests.Session() as session:
        options = getoptions(args[1:])

        sessionconfig(session, config, options)

        execcmd = 'c' in options
        execinter = 'i' in options

        if execcmd:
            process_cmd(options['c'], url, session)

        if execinter or not execcmd:
            interactive(url, session)


if __name__ == '__main__':
    main(sys.argv)
