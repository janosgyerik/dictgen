Webster's Unabridged Dictionary by Various
==========================================

From: http://www.gutenberg.org/ebooks/29765


Parsing
-------

1. Download the plain text file from the website

2. Create a cleaned file:
    - cut out text before "A" (the first entry)
        - but leave 2 blank lines before it
    - cut out text after "ZYTHUM" (the last entry)
	- add back a blank line, followed by "THE END" (will be discarded)
    - change to unix format
    - add a blank line before "GAPES; THE GAPES" and after "The gapes."
    - add a blank line before "HINDOOISM"
    - delete "M." line before "LYMPHOGENIC"
    - delete "P." line before "OZONIC"
    - delete "X." line before "WYND"

    An already cleaned file is here (10 MB download, 27 MB unzipped):

    http://data.janosgyerik.com/pub/webdict/wud/clean.1.gz

3. Run `./gen.py path/to/clean.1` to generate the index and entry files.

    You might want to run with the `-h` flag first to see options.
    To test run without creating files, run like this:

        ./gen.py --dry-run -c 15 path/to/clean.1

An already parsed and zipped output is here:

http://data.janosgyerik.com/pub/webdict/wud/wud.tar.gz


License
-------

See license.txt included in this directory, or this link:

http://www.gutenberg.org/wiki/Gutenberg:The_Project_Gutenberg_License#The_Full_Project_Gutenberg_License_in_Legalese_.28normative.29
