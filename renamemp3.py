import mp3_tagger
import os
import sys
import re


def special_cases(artist, full_artist, song):

    if full_artist == 'Marc Maron':
        return "WTF", song
    return artist, song


def get_new_filename(old_filename, do_full_artist=False, quiet=True):
    m = mp3_tagger.MP3File(old_filename)
    tags = m.get_tags()

    if 'artist' not in tags['ID3TagV2'] and 'song' not in tags['ID3TagV2']:
        if not quiet:
            print "\t%s          (no tags found, not renaming)" % (old_filename.ljust(50), )
        return None

    full_artist = tags['ID3TagV2']['artist'].encode('utf-8') if 'artist' in tags['ID3TagV2'] else "No Artist"
    song = tags['ID3TagV2']['song'].encode('utf-8') if 'song' in tags['ID3TagV2'] else "No Song"
    track = tags['ID3TagV1']['track']  # not sure what to do with this...
    if do_full_artist:
        artist_name = full_artist
    else:
        # use artist's initials, keep case
        artist_name = "".join([a for i, a in enumerate(full_artist) if (i == 0 or full_artist[i - 1] == ' ')])
    # strip out bad chars
    song_clean = "".join([a for a in song if ((a >= 'A' and a <= 'Z') or (a >= 'a' and a <= 'z') or (a == ' ') or (a >= '0' and a <= '9'))])
    song_clean = re.sub(' *$', '', song_clean)
    artist_name, song_clean = artist_name.lstrip().rstrip(), song_clean.lstrip().rstrip()
    artist_name, song_clean = special_cases(artist_name, full_artist, song_clean)
    out_file = "%s - %s.mp3" % (artist_name, song_clean)
    if not quiet:
        print "\t%s %s %s" % (old_filename.ljust(50), ("%s" % (track, )).ljust(8), out_file)
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
    matching = [f for f in files if f.endswith('mp3')]  # re.match("^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}.*\.mp3", f)]
    renames = []

    print "\nScanning...\n"
    print "\tMatching MP3 found                                 Track    Rename to"
    for c in matching:
        out_file = get_new_filename(c, do_full_artist=do_full, quiet=False)
        if out_file is None:
            continue
        cmd = 'mv "%s" "%s"' % (c, out_file)
        renames.append(cmd)
    print "\nPaste these commands to terminal to rename mp3 files:\n"

    for c in renames:
        print c
    print "\n"
