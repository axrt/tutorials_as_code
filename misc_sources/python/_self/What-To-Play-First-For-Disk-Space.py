#!/usr/bin/env python
"""
What-To-Play-First-For-Disk-Space
Shows sorted mediafiles with ratio of file-size to play-time.
"""

import os
import pprint
import string
import subprocess
import sys


def playtime_in_seconds(mediafile):
    cmd = "ffprobe -show_entries format=duration -v quiet -of csv=\"p=0\" -i \"%s\"" % (mediafile)
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()


def file_size_in_bytes(mediafile):
    return os.path.getsize(mediafile)


def filetype_is_media(filepath):
    if filepath.lower().endswith(('.mp4', '.mkv', '.flv', '.avi', '.mpg',
                                  '.mpeg', '.ogv', '.vob', '.webm', '.3gp',
                                  '.3gpp', '.wmv', '.m4v', '.m4p', '.mov',
                                  '.rm', '.rmvb', '.asf', '.3g2')):
        return True
    if filepath.lower().endswith(('.wav', '.mp3', '.flac', '.ogg', '.m4a',
                                  '.vox', '.au', '.oga', '.wma', '.wv')):
        return True
    return False


def mediafiles_spec(path, files):
    mediafiles = []
    for file in files:
        spec = { "filename": os.path.join(path, file) }
        try:
            spec["length"] = string.atof(playtime_in_seconds(spec["filename"]))
        except:
            continue
        if not filetype_is_media(file):
            continue
        spec["size"] = file_size_in_bytes(spec["filename"])
        #spec["ratio"] = spec["size"] / spec["length"]
        mediafiles.append(spec)
    return mediafiles


def path_walker(dirpath):
    mediafiles = []
    for (path, dirs, files) in os.walk(dirpath):
        mediafiles += mediafiles_spec(path, files)
    #return sorted(mediafiles, key=lambda k: k['size']/k['length'], reverse=True)
    return sorted(mediafiles, key=lambda k: (k['size']/k['length'], k['size']), reverse=True)


def media_title_from_spec(spec):
    return "%dMB %dmin :: %s" % (spec["size"]/(1024*1024.0),
                                 spec["length"]/60,
                                 spec["filename"].split("/")[-1])


def mediafiles_to_stdout(mediafiles):
    for media in mediafiles:
        pprint.pprint(media_title_from_spec(media))
        pprint.pprint("path: %s" % media["filename"])


def mediafiles_to_m3u(mediafiles, filename):
    with open(filename, 'w') as m3u:
        for media in mediafiles:
            m3u.write("# %s\n" % (media_title_from_spec(media)))
            m3u.write("%s\n" % (media["filename"]))


def mediafiles_to_pls(mediafiles, filename):
    with open(filename, 'w') as pls:
        pls.write("[playlist]\n")
        pls.write("NumberOfEntries=%d\n" % (len(mediafiles)))
        pls.write("Version=2\n")
        pls.write("\n")
        _index = 1
        for media in mediafiles:
            pls.write("Title%d=%s\n" % (_index, media_title_from_spec(media)))
            pls.write("File%d=%s\n" % (_index, media["filename"]))
            pls.write("\n")
            _index += 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: %s <Path-To-Media-Dir> <Output-Option>" % (sys.argv[0]))
        sys.exit(1)
    if sys.argv[1] in ["--help", "-help", "help", "-h"]:
        pprint.pprint(self.__doc__)
    mediapath = sys.argv[1]
    output = "stdout"
    if len(sys.argv) > 2:
        output = sys.argv[2]

    mediafiles = path_walker(mediapath)
    if output.lower().endswith('.m3u'):
        mediafiles_to_m3u(mediafiles, output)
    elif output.lower().endswith('.pls'):
        mediafiles_to_pls(mediafiles, output)
    else:
        mediafiles_to_stdout(mediafiles)