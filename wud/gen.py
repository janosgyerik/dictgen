#!/usr/bin/env python

import logging
import os
import re

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
        fh.write(content)


def is_new_term(line, prev_line_blank):
    return re_entry_start.match(line) and prev_line_blank and '  ' not in line


def parse_content(arg):
    prev_line_blank = True
    term = None
    term_count = 0
    content = []
    with open(arg) as fh:
        for line0 in fh:
            line = line0.strip()
            if is_new_term(line, prev_line_blank):
                if term:
                    for term in term.split('; '):
                        yield term, '\n'.join(content) + '\n'
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
    def next_index_entry():
        count = 0
        for term, content in parse_content(arg):
            count += 1
            if max_count and count > max_count:
                break
            dirname, filename = get_split_path(term, count)
            entry = '{}/{}:{}'.format(dirname, filename, term)
            logging.info(entry)
            yield entry, dirname, filename, content

    if dry_run:
        for _ in next_index_entry():
            pass
    else:
        if not os.path.isdir(DATA_DIR):
            os.makedirs(DATA_DIR)
        with open(INDEX_PATH, 'w') as fh:
            for entry, dirname, filename, content in next_index_entry():
                fh.write(entry + '\n')
                write_entry_file(dirname, filename, content)


def main():
    parser = ArgumentParser(description='Generate index and entry files '
                                        'from cleaned plain text file')
    parser.add_argument('--dry-run', '-d', '-n', action='store_true',
                        help="Dry run, don't write to files")
    parser.add_argument('--max-count', '-c', type=int,
                        help="Exit after processing N records")
    parser.add_argument('files', help="File(s) to parse", nargs='+')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s: %(message)s')

    for arg in args.files:
        parse_file(arg, dry_run=args.dry_run, max_count=args.max_count)


if __name__ == '__main__':
    main()
