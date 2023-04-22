#!/usr/bin/env python3

import argparse
import os
import json

from .connect import ZeroconfConnect


def read_password_from_file():
    path = os.environ.get('FILE__ZEROSPOT_PASSWORD')
    if path and os.path.exists(path):
        with open(path, 'r') as file:
            return file.readline()
    return ''


def main():
    parser = argparse.ArgumentParser(                    
        prog='zerospot',
        description="Connect to a Spotify zeroconf device on the local net\n"
        "All parameters can be specified in environmental variables prefixed with 'ZEROSPOT_'. e.g. ZEROSPOT_USERNAME\n"
        "The password can be read from a file which's location is stored in FILE__ZEROSPOT_PASSWORD\n"
        "Encrypts Spotify username and password and sends it to the device which will log in on it's own\n\n"
        
        "Only password based login is supported in this script even though Spotify supports token based login too.\n",
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--config', help='Config file path. default: ~/.config/zerospot/config.json',
                        default=os.environ.get('HOME', '') + '/.config/zerospot/config.json')
    parser.add_argument('uri', help='full uri of the zerconf device. e.g. "192.168.1.100:1234/".\n'
                                    'If this are set then --host, --port and --path are ignored.',
                        nargs='?')
    parser.add_argument('--host', help='IP or hostname of the zeroconf device.')
    parser.add_argument('--port', help='port on which the device is listening.')
    parser.add_argument('--path', help='path that can be used to access zeroconf options. default: \"/\"')
    parser.add_argument('--username', help='Spotify username to send')
    parser.add_argument('--password', help='Spotify password to send')

    args = parser.parse_args()

    config = {}
    if os.path.exists(args.config):
        with open(args.config, 'r') as f:
            config = json.loads(f.read())
    
    uri  = args.uri  or os.environ.get('ZEROSPOT_URI')  or config.get('uri')
    host = args.host or os.environ.get('ZEROSPOT_HOST') or config.get('host')
    port = args.port or os.environ.get('ZEROSPOT_PORT') or config.get('port')
    path = args.path or os.environ.get('ZEROSPOT_PATH') or config.get('path') or '/'
    username = args.username or os.environ.get('ZEROSPOT_USERNAME') or config.get('username')
    password = args.password or read_password_from_file() \
               or os.environ.get('ZEROSPOT_PASSWORD') or config.get('password')

    if not uri and (not host or not host):
        parser.error('either uri or both host and port must be provided.')

    if not username or not password:
        parser.error('missing credentials')

    uri = uri or f'{host}:{port}{path}'
    uri = uri if uri.startswith('http://') else 'http://' + uri

    zc = ZeroconfConnect(uri, username, password)

    if zc.connect():
        print(f'Credentials of {username} sent successfully.')
    else:
        print('Something went wrong.')

if __name__ == '__main__':
    main()