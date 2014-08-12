#!/usr/bin/env python

import re
import os

from argparse import ArgumentParser

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
    term_count = 0
    content = []
    with open(arg) as fh:
        for line0 in fh:
            line = line0.strip()
            if re_entry_start.match(line) and prev_line_blank and '  ' not in line:
                if term:
                    for term in term.split('; '):
                        yield term, content
                prev_term = term
                term = line.lower()
                if term == prev_term:
                    term_count += 1
                    subscript = '-' + str(term_count)
                else:
                    term_count = 1
                    subscript = ''
                content = [term + subscript]
            else:
                content.append(line)
            prev_line_blank = not line


def get_split_path(term, count):
    slug = re_nonalpha.sub('_', term.lower()).ljust(3, '_')
    dirname = os.path.join(slug[0], slug[:2], slug[:3])
    filename = '{}-{}.txt'.format(slug, count)
    return dirname, filename


def parse_file(arg, dry_run=False, max_count=0):
    def rebuild_index():
        count = 0
        for term, content in parse_content(arg):
            count += 1
            if max_count and count > max_count:
                break
            dirname, filename = get_split_path(term, count)
            entry = '{}/{}:{}'.format(dirname, filename, term)
            print(entry)
            if not dry_run:
                fh.write(entry + '\n')
                write_entry_file(dirname, filename, content)
    if dry_run:
        rebuild_index()
    else:
        if not os.path.isdir(DATA_DIR):
            os.makedirs(DATA_DIR)
        with open(INDEX_PATH, 'w') as fh:
            rebuild_index()


def main():
    parser = ArgumentParser(description='Generate index and entry files from cleaned plain text file')
    parser.add_argument('--dry-run', '-d', '-n', action='store_true',
                        help="Dry run, don't write to files")
    parser.add_argument('--max-count', '-c', type=int,
                        help="Exit after processing N records")
    parser.add_argument('files', help="File(s) to parse", nargs='+')
    args = parser.parse_args()

    for arg in args.files:
        parse_file(arg, dry_run=args.dry_run, max_count=args.max_count)

if __name__ == '__main__':
    main()
