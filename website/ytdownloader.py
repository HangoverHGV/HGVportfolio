import os, shutil
from pytube import Playlist, YouTube
import string, random
from .zip import ZipCreator


def RandomName():
    return ''.join(random.choice(string.ascii_letters) for x in range(5))


def FolderNotExists(name):
    path = 'Music/' + name
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)


def Delete():
    path = 'Music/'
    count = 0
    for dir in os.listdir(path):
        count += 1

    if count > 5:
        for dir in os.listdir(path):
            pathToDelete = os.path.join(path, dir)
            shutil.rmtree(pathToDelete)


def SongDownload(link):
    if not os.path.exists('Music/'):
        os.makedirs('Music/')
    Delete()
    yt = YouTube(link)
    name = RandomName()
    FolderNotExists(name)
    dest = 'Music/' + name
    video = yt.streams.last()
    out_file = video.download(output_path=dest)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    print(os.listdir('Music'))
    return new_file


def PlaylistDownload(link):
    if not os.path.exists('Music/'):
        os.makedirs('Music/')
    Delete()
    name = RandomName()
    FolderNotExists(name)
    dest = 'Music/' + name
    p = Playlist(link)
    for video in p.videos:
        try:
            audio = video.streams.get_audio_only()
            out_file = audio.download(output_path=dest)
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
        except:
            pass

    zipfile = ZipCreator(dest)
    return zipfile