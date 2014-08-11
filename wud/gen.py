#!/usr/bin/env python

import re
import os

from optparse import OptionParser

DATA_DIR = 'data'
INDEX_PATH = os.path.join(DATA_DIR, 'index.dat')

re_entry_start = re.compile(r'[A-Z][A-Z0-9 ;\'-.,]*$')
re_nonalpha = re.compile(r'[^a-z]')


def write_entry_file(dirname, filename, content):
    basedir = os.path.join(DATA_DIR, dirname)
    if not os.path.isdir(basedir):
        os.makedirs(basedir)

    path = os.path.join(basedir, filename)
    with open(path, 'w') as fh:
        fh.write('\n'.join(content) + '\n')


def parse_content(arg):
    prev_line_blank = True
    term = None
    content = []
    with open(arg) as fh:
        for line0 in fh:
            line = line0.strip()
            if re_entry_start.match(line) and prev_line_blank and '  ' not in line:
                if term:
                    for term in term.split('; '):
                        yield term, content
                term = line.lower()
                content = [line]
            else:
                content.append(line)
            prev_line_blank = not line


def get_split_path(term, count):
    slug = re_nonalpha.sub('_', term.lower()).ljust(3, '_')
    dirname = os.path.join(slug[0], slug[:2], slug[:3])
    filename = '{}-{}.txt'.format(slug, count)
    return dirname, filename


def parse_file(arg, debug=False):
    def rebuild_index():
        count = 0
        for term, content in parse_content(arg):
            count += 1
            if debug and count > 25:
                break
            dirname, filename = get_split_path(term, count)
            entry = '{}/{}:{}'.format(dirname, filename, term)
            print(entry)
            if not debug:
                fh.write(entry + '\n')
                write_entry_file(dirname, filename, content)
    if debug:
        rebuild_index()
    else:
        if not os.path.isdir(DATA_DIR):
            os.makedirs(DATA_DIR)
        with open(INDEX_PATH, 'w') as fh:
            rebuild_index()


def main():
    parser = OptionParser()
    parser.set_usage('%prog [options] file...')
    parser.add_option('--debug', '-d', help="Debug mode, don't write to files", action='store_true')
    parser.set_description('Generate index and entry files from cleaned plain text file')
    (options, args) = parser.parse_args()

    if args:
        for arg in args:
            parse_file(arg, debug=options.debug)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
