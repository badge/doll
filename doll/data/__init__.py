from os import mkdir
from sys import stdout
from os.path import exists, expanduser, isdir, join
from urllib.request import urlopen
from zipfile import ZipFile


def _doll_dir(create: bool = False):
    """Find or create the doll data directory

    :param create: whether to create the directory if it doesn't exist
    :type create: bool

    :return the directory, whether pre-existing or just-created
    """

    doll_dir = expanduser("~/.doll")

    if not exists(doll_dir):
        if not create:
            raise RuntimeError("doll data directory does not exist and was not created at {}\n"
                               "(rerun with create=True to create.)".format(doll_dir))
        print("Creating ~/.doll directory")
        try:
            mkdir(doll_dir)
        except OSError:
            raise RuntimeError("Could not create doll data directory at {}".format(doll_dir))
    else:
        if not isdir(doll_dir):
            raise RuntimeError("{0} exists but is not a directory".format(doll_dir))
        else:
            print("~/.doll directory already exists and was not created.")

    return doll_dir


def download(create_dir: bool = False):
    """Download and extract the Words source files

    :param create_dir: whether to create the directory if it doesn't exist
    :type create_dir: bool

    :return None
    """

    words_all = 'wordsall'
    words_url = 'http://archives.nd.edu/whitaker/wordsall.zip'
    data_dir = _doll_dir(create=create_dir)

    url = urlopen(words_url)

    # Download the file
    with open(join(data_dir, words_all + '.zip'), 'wb') as file:
        file_size = int(url.headers["Content-Length"])
        print('Downloading {}.zip ({:,} bytes)'.format(words_all, file_size))

        fetch_size = 0
        block_size = 1024 * 64

        while True:
            data = url.read(block_size)
            if not data:
                break

            fetch_size += len(data)
            file.write(data)

            status = '\r{:12,} bytes [{:5.1f}%]'.format(fetch_size, fetch_size * 100.0 / file_size)
            stdout.write(status)
            stdout.flush()

    # Unpack the file
    print('\nUnpacking {}'.format(words_all + '.zip'))

    with ZipFile(join(data_dir, words_all + '.zip'), 'r') as zip_file:
        zip_file.extractall(join(data_dir, words_all))

    print('{} downloaded and extracted at {}'.format(words_all, data_dir))
