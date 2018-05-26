# renamemp3

Rename mp3 files from a UUID (common to many podcast hosting sites) to something human-readable. E.g.:

    `09c2efd1-9b80-4696-a412-59d1d51522bc.mp3`

becomes:

    `ID10T with Chris Hardwick - Natalie Dormer.mp3`

or, with the artist's name abbreviated:

    `IwCH - Natalie Dormer.mp3`


### Syntax

In the directory containing the MP3 files, run:

    python renamemp3.py

Use the option `-f` or `--full_artist` to use the entire artist string.

This scans the CWD for files matching the format <UUID>.mp3, reads the mp3 tag strings and suggests an output filename for each file found.

The files are not renamed, but the commands to rename them are printed, so you just have to copy & paste them to the command line.

#### Requirements
python

`mp3_tagger` python module