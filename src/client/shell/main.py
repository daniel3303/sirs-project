import sys
import requests
from commands import *


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


def authenticate(sess, opts):
    username = opts.get('u') or opts.get('username')
    password = opts.get('p') or opts.get('password')
    sess.auth = username, password


def sessionconfig(sess, config, opts):
    cert = config['cert']
    sess.verify = cert
    authenticate(sess, opts)


def help(*params):
    print('Usage:')
    print(' ', 'python main.py [-c <command>] [-i] [-u <username>] [-p <password>]')

    print('Options:')
    print(' ', '-c <command>')
    print('     ', 'Executes the command <command>')
    print(' ', '-i')
    print('     ', 'Enters in interactive mode to execute commands')
    print(' ', '-u, --username <username>')
    print('     ', 'Configs the username <username> to be used to login')
    print('     ', 'Should be used together with --password option')
    print(' ', '-p, --password <password>')
    print('     ', 'Configs the password <password> to be used to login')
    print('     ', 'Should be used together with --username option')

    print('Commands available:')
    print(' ', 'register username=<username> password=<password>')
    print(' ', 'ls')
    print(' ', 'create name=<file_name>')
    print(' ', 'change id=<file_id> content=<new_file_content>')
    print(' ', 'download id=<file_id> name=<file_name>')
    print(' ', 'delete id=<file_id>')
    print(' ', 'upload name=<server_file_name> file=<file_name>')
    print(' ', 'login username=<username> password=<password>')


cmdprocessors = {
    'help': help,
    'ls': ls,
    'test': test,
    'upload': upload,
    'download': download,
    'register': register_user,
    'create': create,
    'change': change,
    'delete': delete,
    'login': lambda url, sess, opt: authenticate(sess, opt)
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


def splitter(string):
    sep = ' '

    initIdx = idx = 0
    insideQuote = False

    parts = []

    for idx in range(len(string)):
        if string[idx] == '"':
            insideQuote = not insideQuote
            continue

        if not insideQuote and string[idx] == sep:
            if initIdx != idx:
                parts.append(string[initIdx: idx])
            initIdx = idx + 1

    idx = idx + 1
    if initIdx != idx:
        parts.append(string[initIdx: idx])

    return [*map(lambda e: e.replace('"', ''), parts)]


def parsecmd(strcmd):
    cmd, *listparams = splitter(strcmd)
    params = {k: v for k, v in (x.split('=', 2) for x in listparams)}
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
