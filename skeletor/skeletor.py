import os
import json
import shutil
import hashlib

# Global configuration variable.
cfg = {}

def set_config():
    cfg['loc'] = os.path.expanduser('~/.skeletor')
    cfg['libname'] = 'skeletor'

    if not os.path.exists(cfg['loc']):
        os.mkdir(cfg['loc'])
        os.mkdir(os.path.join(cfg['loc'], '_files'))

set_config()


def read_template(filelist):
    """Read the specificed directories and files into 
    the internal format."""

    tmp = {'.': []}

    # Convert to an array of strings.
    if isinstance(filelist, str):
        filelist = [filelist]

    for f in filelist:

        # If it's just a file, store it.
        if os.path.isdir(f):
            for root, dirs, files in os.walk(f):
                tmp[root] = files

        else:
            tmp['.'].append(f)

    return tmp


def save_template(name, data):
    """Save the structure of the template to a the 
    module's storage location for later use."""

    # Link the filenames to hashed files
    for path in data:
        for i, file in enumerate(data[path]):
            src = os.path.join(path, file)
            m = hashlib.new('ripemd160')
            m.update(open(src).read())
            dest = os.path.join(cfg['loc'], '_files', m.digest())

            data[path][i] = ':'.join([file, m.digest()])
            shutil.copyfile(src, dest)

    if '.' in name:
        domain, kind = name.split('.')
    else:
        domain = cfg['libname']
        kind = name

    fname = os.path.join(cfg['loc'], domain + '.json')

    if os.path.exists(fname):
        domain_string = open(fname, 'r').read()
    else:
        domain_string = ''

    if domain_string == '':
        tmp = {}
    else:
        tmp = json.loads(domain_string)

    tmp[kind] = data

    f = open(fname, 'w')
    json.dump(tmp, f, indent=2, sort_keys=True)


def dump_template(name, dest):
    """Load a template that's been saved and start a new
    project."""

    if '.' in name:
        domain, kind = name.split('.')
    else:
        domain = cfg['libname']
        kind = name

    fname = os.path.join(cfg['loc'], domain + '.json')
    domain_data = json.load(open(fname, 'r'))

    if kind not in domain_data.keys():
        print('Template does not exist.')
        return

    # Load the template format.
    tmp = domain_data[kind]

    # Now beging making a new project from the template.
    if not os.path.exists(dest):
        os.mkdir(dest)

    for path in tmp.keys():

        newpath = os.path.join(dest, path)

        if not os.path.exists(newpath):
            os.makedirs(newpath)

        for file in tmp[path]:

            fname, skname = file.split(':')

            src = os.path.join(cfg['loc'], '_files', skname)
            dst = os.path.join(newpath, fname)
            shutil.copy(src, dst)

def get_domain_list(domain='skeletor'):
    """List all the kinds of templates in a particular domain."""

    fname = os.path.join(cfg['loc'], domain + '.json')
    domain_data = json.load(open(fname, 'r'))

    return domain_data.keys()


