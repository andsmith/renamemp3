import mp3_tagger
import os
import sys
import re


def get_new_filename(old_filename, do_full_artist=False, quiet=True):
    m = mp3_tagger.MP3File(old_filename)
    tags = m.get_tags()

    artist = tags['ID3TagV2']['artist'].encode('utf-8')
    song = tags['ID3TagV2']['song'].encode('utf-8')
    track = tags['ID3TagV1']['track']  # not sure what to do with this...
    if do_full_artist:
        artist_name = artist
    else:
        # use artist's initials, keep case
        artist_name = "".join([a for i, a in enumerate(artist) if (i == 0 or artist[i - 1] == ' ')])
    # strip out bad chars
    song_clean = "".join([a for a in song if ((a >= 'A' and a <= 'Z') or (a >= 'a' and a <= 'z') or (a == ' ') or (a >= '0' and a <= '9'))])
    song_clean = re.sub(' *$', '', song_clean)
    out_file = "%s - %s.mp3" % (artist_name, song_clean)
    if not quiet:
        print "\t%s %s %s" % (old_filename, ("%s" % (track, )).ljust(6), out_file)
    return out_file


if __name__ == "__main__":
    do_full = False
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-f', '--full_artist']:
            do_full = True
        else:
            print "Unknown command."
            print "Syntax:  python renamemp3.py [-f|--full-artist]"
            sys.exit()

    files = [f for f in os.listdir('.') if f.lower().endswith('mp3')]
    matching = [f for f in files if re.match("^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}.*\.mp3", f)]
    renames = []

    print "\nScanning...\n"
    print "\tMatching MP3 found                       Track  Rename to"
    for c in matching:
        out_file = get_new_filename(c, do_full_artist=do_full, quiet=False)
        cmd = 'mv "%s" "%s"' % (c, out_file)
        renames.append(cmd)
    print "\nPaste these commands to terminal to rename mp3 files:\n"

    for c in renames:
        print c
    print "\n"
