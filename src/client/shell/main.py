import itertools
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


def authenticate(url, sess, opts):
    username = opts.get('u') or opts.get('username')
    password = opts.get('p') or opts.get('password')

    if username is not None and password is not None:
        params = {'username': username, 'password': password}

        valid = check_credentials_validity(url, sess, params)
        if valid:
            sess.auth = username, password
            return
    else:
        print('You\'re not authenticated')

    sess.auth = None, None


def sessionconfig(sess, config, opts):
    cert = config['cert']
    sess.verify = cert
    authenticate(opts['url'], sess, opts)


def commandshelp():
    print('Commands available:')
    print(' ', 'register username=<username> password=<password> name=<user\'s name>')
    print('     ', 'Register the user <user\'s name> with username <username> and password <password>')
    print(' ', 'login username=<username> password=<password>')
    print('     ', 'Login with username <username> and password <password>')
    print(' ', 'ls')
    print('     ', 'List files')
    print(' ', 'create name=<server_file_name>')
    print('     ', 'Create a remote file with name <server_file_name>')
    print(' ', 'change id=<file_id> [content=<new_file_content>] [name=<new_file_name>]')
    print('     ', 'Change content and/or name of the remote file <file_id>')
    print(' ', 'download id=<file_id> [file=<file_name>] [location=<dir_path>]')
    print('     ', 'Download remote file <file_id> and save as <file_name> in the directory <dir_path>')
    print('     ', 'Default <dir_path> is application folder downloads')
    print('     ', 'Default <file_name> is the remote file name')
    print(' ', 'delete id=<file_id>')
    print('     ', 'Delete remote file <file_id>')
    print(' ', 'upload name=<server_file_name> file=<file_name>')
    print('     ', 'Upload local file <file_name> as <server_file_name>')
    print(' ', 'check id=<file_id>')
    print('     ', 'Check user permissions over the file <file_id>')
    print(' ', 'manage fileId=<file_id> userId=<user_id> read=[True|False] write=[True|False]')
    print('     ', 'Change the user <user_id> permissions over the file <file_id>')
    print('     ', 'The parameters "read" and "write" are the permissions to be set')
    print(' ', 'users')
    print('     ', 'List all the users')
    print(' ', 'read id=<file_id> [numbered=[TRUE|FALSE]]')
    print('     ', 'Show file <file_id> content')
    print('     ', 'Parameter "numbered" sets on/off the number lines')
    print(' ', 'write id=<file_id> content=<content_to_insert> after=<line_number>')
    print('     ', 'Writes <content> in the file <file_id> after line <line_number>')
    print(' ', 'append id=<file_id> content=<content_to_append>')
    print('     ', 'Appends <content> in end of the file <file_id>')
    print(' ', 'replace id=<file_id> line=<line_number> content=<new_line_content>')
    print('     ', 'Replaces the line <line_number>\'s content by <content> in the file <file_id>')
    print(' ', 'erase id=<file_id> line=<line_number>')
    print('     ', 'Erases the line <line_number> in the file <file_id>')


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

    commandshelp()


cmdprocessors = {
    'help': help,
    'ls': ls,
    'upload': upload,
    'download': download,
    'register': register_user,
    'create': create,
    'change': change,
    'delete': delete,
    'login': authenticate,
    'check': check_permissions,
    'manage': manage_permissions,
    'users': list_users,
    'read': read,
    'write': write,
    'append': append,
    'replace': replace,
    'erase': erase
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
    listparams = list(itertools.filterfalse(lambda p: '=' not in p, listparams))
    params = {k: v for k, v in (p.split('=', 2) for p in listparams)}
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
        options['url'] = url

        sessionconfig(session, config, options)

        execcmd = 'c' in options
        execinter = 'i' in options

        if execcmd:
            process_cmd(options['c'], url, session)

        if execinter or not execcmd:
            interactive(url, session)


if __name__ == '__main__':
    main(sys.argv)
