import os
import sys
import base64
import getpass
import configparser
import requests


def check_startup():

    startup_vars = {}

    print('Checking to see if os.environ has the required settings...')

    if ('ISE_SERVER' and 'ISE_TOKEN') in os.environ:
        server = os.environ.get('ISE_SERVER')
        token = os.environ.get('ISE_TOKEN')
        print('From OS environ: server =', server)
        print('From OS environ: token =', token)


    config = configparser.ConfigParser()
    #config_file_path = config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'startup.cfg'))
    #config_file_path = os.path.join(os.getcwd(),'startup.cfg')
    config_file_path = './startup.cfg'
    #config_file_path = 'startup.cfg'
    config.read(config_file_path)

    if config.has_section('servers'):
        print('Testing that startup.cfg has_section(servers) is in config')
    else:
        print('nada servers section')

    if config.has_section('authorization'):
        print('Testing that startup.cfg has_section(authorization) is in config')
    else:
        print('nada authorization section')

    if not (('ISE_SERVER' and 'ISE_TOKEN') in os.environ):
        server = config.get('servers', 'ise_server')
        print('From startup.cfg: server =', server)
        token = config.get('authorization', 'ise_token')
        print('From startup.cfg: token =', token)


    if (server == '' or token == ''):
        if (server == ''):
            server = input('Enter the ISE Server IP Address:')
        if (token == ''):
            print('Enter your ISE NB API username and password to generate your Basic Auth token.')
            userId = input('Username:')
            passwd = getpass.getpass()
            userPass = userId + ':' + passwd
            base64Val = base64.b64encode(userPass.encode())
            token = base64Val.decode()
            print('Your Base64 Encoded token is = {}.\n\n'.format(token))
            print('If you entered your username\password incorrectly you can run getToken.py and update startup.cfg')

        config.set('servers', 'ise_server', server)
        config.set('authorization', 'ise_token', token)

        print('ISE: Contents to be written to startup.cfg: server = {} ; token = {}.\n\n'.format(server, token))

        with open('startup.cfg', 'w') as config_file:
            config.write(config_file)

    headers = {
        "authorization": "Basic " + token,
        "accept": "application/vnd.com.cisco.ise.ca.endpointcert.1.0+xml;charset=UTF-8",
    }


    url = 'https://' + server + ':9060/ers/config/endpointcert/versioninfo'

    print('Trying connection to ISE server : {} ...'.format(server))
    try:
        resp = requests.get(url, headers=headers, timeout=25, verify=False)
        resp.raise_for_status()
    except requests.exceptions.Timeout as err:
        print('\n', err)
        print('ISE server appears to be unreachable!!')
        sys.exit(1)
    except requests.exceptions.HTTPError as err:
        print('\n', err)
        if resp.status_code == 401:
            print("Looks like your token is invalid. \n"
                  "Ensure you used the correct username and password.\n"
                  "Run getToken.py to generate a new token and update it in startup.cfg.\n\n")
            sys.exit()
        else:
            print('HTTPError: Check error code', resp.status_code)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        print('\n', err)
        print('RequestException')
        sys.exit(1)

    if resp.status_code == 200:
        print('Status code={}. Making calls to ISE server: {}\n'.format(resp.status_code, server))

    startup_vars['server'] = server
    startup_vars['token'] = token

    return startup_vars

