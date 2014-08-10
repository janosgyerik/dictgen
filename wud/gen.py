#!/usr/bin/env python

import re
import os

from optparse import OptionParser

DATA_DIR = 'data'
INDEX_PATH = os.path.join(DATA_DIR, 'index.dat')

re_entry_start = re.compile(r'[A-Z][A-Z0-9 ;\'-.,]*$')
re_nonalpha = re.compile(r'[^a-z]')


def get_filename(term, count):
    slug = re_nonalpha.sub('_', term.lower())
    dirname = slug.ljust(2, '0')[:2]
    filename = slug + '-' + str(count)
    return dirname, filename + '.txt'


def write_entry_file(dirname, filename, content):
    basedir = os.path.join(DATA_DIR, dirname)
    if not os.path.isdir(basedir):
        os.makedirs(basedir)

    path = os.path.join(basedir, filename)
    print '* writing to file', path
    with open(path, 'w') as fh:
        fh.write(content)


def append_to_index(dirname, filename, term):
    with open(INDEX_PATH, 'a') as fh:
        fh.write('{}/{}:{}\n'.format(dirname, filename, term.lower()))


def parse_file(arg):
    prev_line_blank = True
    prev_prefix = '0'
    term = None
    content = ''
    count = 1
    if os.path.isfile(INDEX_PATH):
        os.remove(INDEX_PATH)
    with open(arg) as fh:
        for line0 in fh:
            line = line0.strip()
            if re_entry_start.match(line) and prev_line_blank and not line.count('  '):
                if term:
                    for term in term.split('; '):
                        dirname, filename = get_filename(term, count)
                        write_entry_file(dirname, filename, content)
                        append_to_index(dirname, filename, term)
                term = line
                content = line0
                if term[0] != prev_prefix:
                    prev_prefix = term[0]
                    count = 1
                count += 1
            else:
                content += line0
            prev_line_blank = not line


def main():
    parser = OptionParser()
    parser.set_usage('%prog [options] file...')
    parser.set_description('Generate index and entry files from cleaned plain text file')
    (options, args) = parser.parse_args()

    if args:
        for arg in args:
            parse_file(arg)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
