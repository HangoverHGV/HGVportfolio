from zipfile import ZipFile
import os


def ZipCreator(dir_path):
    dir_path = 'website/' + dir_path
    print(dir_path)
    with ZipFile('yourDownload.zip', 'w') as myZip:
        for path in os.listdir(dir_path):
            file = os.path.join(dir_path, path)
            if os.path.isfile(file):
                myZip.write(file)

    os.rename('yourDownload.zip', dir_path + '/yourDownload.zip')
    zipFile = dir_path + '/yourDownload.zip'
    return zipFile