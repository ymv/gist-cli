#!/usr/bin/env python
import argparse
import ConfigParser
import os.path
import urllib2
import json
import sys
import base64

def die(message, *args):
    sys.stderr.write(message % args + '\n')
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser( description = 'Create a github gist from a file, or from stdin' )
    parser.add_argument( 'infile_list', nargs = '*', type = argparse.FileType( 'r' ))
    parser.add_argument( '--description', '-d', default = '' )
    parser.add_argument( '--private', '-p', action = 'store_true', default = False )
    parser.add_argument( '--anonymous', '-a', action = 'store_true', default = False )
    parser.add_argument( '--stdin-file-name', default='stdin')
    parser.add_argument( '--verbose', '-v', action = 'store_true', default = False )
    arguments = parser.parse_args()

    if len(arguments.infile_list) > 0:
        files = {}
        for infile in arguments.infile_list:
            name = os.path.basename(infile.name)
            if name in files:
                die('Duplicate file name after path striping: %s', infile.name)
            files[name] = {'content': infile.read()}
    else:
        files = {arguments.stdin_file_name: {'content': sys.stdin.read()}}

    request = urllib2.Request( 'https://api.github.com/gists' )

    if not arguments.anonymous:
        gitconfig = ConfigParser.ConfigParser()
        try:
            gitconfig.readfp( open( os.path.expanduser( '~/.gitconfig' ) ) )
            username = gitconfig.get( 'github', 'user' )
            password = gitconfig.get( 'github', 'password' )
        except ConfigParser.Error as e:
            die('Invalid auth config: %s', e.message)
        raw = '%s:%s' % (username, password)
        auth = 'Basic %s' % base64.b64encode(raw).strip()
        request.add_header('authorization', auth)

    request.add_data(json.dumps( {
        'description': arguments.description,
        'public': not arguments.private,
        'files': files,
    }))

    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError as e:
        if e.code == 401:
            die('Invalid username/password')
        die('API HTTP error: %d %s', e.code, e.reason)

    json_response = json.loads(response.read())
    if arguments.verbose:
        json.dump(json_response, sys.stdout, sort_keys=True, indent=2)
    else:
        print json_response['html_url']

if __name__ == '__main__':
  main()
