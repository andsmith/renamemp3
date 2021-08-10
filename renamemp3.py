import mp3_tagger
import os
import sys
import re
import argparse


def special_cases(artist, full_artist, song):

    if full_artist in ['Marc Maron']:
        return "WTF", song

    elif full_artist in ['Behind the Bastards']:
        header_searchers = [re.compile("^[Pp]art [Oo]ne (.*)$"),
                            re.compile("^[Pp]art [Tt]wo (.*)$"),
                            re.compile("^[Pp]art [Tt]hree (.*)$"),
                            re.compile("^[Pp]art [Ff]our (.*)$"),
                            re.compile("^[Pp]art [Ff]ive (.*)$"),
                            re.compile("^[Pp]art [Ss]ix (.*)$")]
        for part_no, header_searcher in enumerate(header_searchers):
            song_title_parts = header_searcher.search(song)
            if song_title_parts is not None:
                song_title = song_title_parts.groups()[0]
                return "BtB", "%s - part %i" % (song_title, part_no + 1)
            
    return artist, song


def get_new_filename(old_filename, do_full_artist=False, quiet=True):

    m = mp3_tagger.MP3File(old_filename)
    try:
        tags = m.get_tags()
    except:
        if not quiet:
            print("\t%s          (no tags found, not renaming)" % (old_filename.ljust(50),))
        return None

    if 'artist' not in tags['ID3TagV2'] and 'song' not in tags['ID3TagV2']:
        if not quiet:
            print("\t%s          (no tags found, not renaming)" % (old_filename.ljust(50),))
        return None
    if 'artist' in tags['ID3TagV2'] and tags['ID3TagV2']['artist'] is not None:
        full_creator = tags['ID3TagV2']['artist'].encode('utf-8')
    elif 'album' in tags['ID3TagV2'] and tags['ID3TagV2']['album'] is not None:
        full_creator = tags['ID3TagV2']['album'].encode('utf-8')
    else:
        full_creator = None
    if full_creator is not None:

        full_creator = full_creator.rstrip().lstrip().decode()
    
        #full_creator = full_creator.rstrip(("\x00".encode())).lstrip(("\x00".encode())).decode()  # necessary?
    
    song = tags['ID3TagV2']['song'].encode('utf-8') if 'song' in tags['ID3TagV2'] and tags['ID3TagV2'][
        'song'] is not None else None
    
    if song is None:
        return None
    song = song.decode()
    
    track = tags['ID3TagV1']['track']  # not sure what to do with this...
    
    if full_creator is not None:
        if do_full_artist:
            artist_name = full_creator
        else:
            # use artist's initials, keep case
            artist_name = "".join([a for i, a in enumerate(full_creator) if (i == 0 or full_creator[i - 1] == ' ')])
        artist_name = artist_name.lstrip().rstrip()
    else:
        artist_name = None
        
    # strip out bad chars

    song_clean = "".join([a for a in song if ((a >= 'A' and a <= 'Z') or
                                              (a >= 'a' and a <= 'z') or
                                              (a == ' ') or
                                              (a >= '0' and a <= '9'))])
    song_clean = re.sub(' *$', '', song_clean)
    song_clean = song_clean.lstrip().rstrip()
    
    artist_name, song_clean = special_cases(artist_name, full_creator, song_clean)

    if artist_name is not None and song_clean is not None:
        out_file = "%s - %s.mp3" % (artist_name, song_clean)
    elif artist_name is not None:
        print("\t%s          (only artist found, could overwrite other tracks!)" % (old_filename.ljust(50),))

        out_file = "%s.mp3" % (artist_name, )
    elif artist_name is not None:
        out_file = "%s.mp3" % (song_clean,)
    else:
        if not quiet:
            print("\t%s          (no artist or song tag, not renaming)" % (old_filename.ljust(50),))
        return None
        

    # remove double spaces
    out_file = re.sub(' +', ' ', out_file)

    if not quiet:
        print("\t%s %s %s" % (old_filename.ljust(50), ("%s" % (track,)).ljust(8), out_file))
    return out_file


def _do_cmd_args():
    parser = argparse.ArgumentParser(description='Rename MP3 files based on internal tags.')
    parser.add_argument('files', type=str, help='File with crime statistics (CSV).', nargs="*")
    parser.add_argument('--full_artist', '-f', help="Don't abbreviate artist's name in filename prefix.",
                        action='store_true', default=False)
    parsed = parser.parse_args()

    return parsed.files, parsed.full_artist


if __name__ == "__main__":
    files, do_full = _do_cmd_args()
    if files is None or len(files) == 0:
        files = [f for f in os.listdir('.') if f.lower().endswith('mp3')]
    matching = files  # re.match("^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}.*\.mp3", f)]
    renames = []

    print("\nScanning...\n")
    print("\tMatching MP3 found                                 Track    Rename to")
    for c in matching:
        out_file = get_new_filename(c, do_full_artist=do_full, quiet=False)
        if out_file is None:
            continue
        cmd = 'mv "%s" "%s"' % (c, out_file)
        renames.append(cmd)
    print("\nPaste these commands to terminal to rename mp3 files:\n")

    for c in renames:
        print(c)
    print("\n")
