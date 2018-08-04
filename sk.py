from skeletor import skeletor

import sys
import argparse

def main():

    parser = argparse.ArgumentParser(description='Use skeletor templating from command line.')

    parser.add_argument('cmd', metavar='c', type=str, nargs='?', default='sk')
    parser.add_argument('name', metavar='n', type=str, nargs='?')
    parser.add_argument('--sources', type=str, nargs='+')
    parser.add_argument('--output-dir', type=str)

    args = parser.parse_args()

    if args.cmd == 'snap':
        tmp = skeletor.read_template(args.sources)
        skeletor.save_template(args.name, tmp)

    if args.cmd == 'spit':
        if args.output_dir is None:
            skeletor.dump_template(args.name, '.')
        else:
            skeletor.dump_template(args.name, args.output_dir)

    if args.cmd == 'list':
        if '.' in args.name:
            domain = args.name.split('.')[0]
        else:
            domain = args.name

        for kind in skeletor.get_domain_list(domain):
            print(kind)

    return 0
