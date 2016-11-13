import os
from ..input_parser.add_database_types import create_type_contents
from ..input_parser.parse_dictionary import parse_dict_file
from ..input_parser.parse_inflections import parse_inflect_file
from ..config import config


def parse_all_inputs(words_dir: str = os.path.expanduser('~/.doll/wordsall'), commit_changes: bool = False):
    """Creates the database and parses all the inputs

    :param words_dir: Directory of wordsall
    :type words_dir: str
    :param commit_changes: Whether to commit changes to the database
    :type commit_changes: bool

    :return None
    """

    # Add a trailing slash if necessary
    if words_dir[-1:] != '/':
        words_dir += '/'

    # First check that our words folder exists
    if not os.path.isdir(words_dir):
        print('Cannot find words_dir at {0}! Exiting...'.format(words_dir))
        return

    # And then that our input files exist
    files_to_find = ['INFLECTS.LAT', 'DICTLINE.GEN']
    error_string = ', '.join([f for f in files_to_find if not os.path.isfile(words_dir + f)])

    if not error_string == '':
        print('Unable to find the following file(s): ' + error_string + '. Exiting...')
        return

    if os.path.isfile(os.path.expanduser("~/.doll/") + config['db_file']):
        if not input('Database file exists, overwrite? (Yes/ No)')[:1] == 'Y':
            print('Database file exists, exiting...')
            return
        else:
            os.remove(os.path.expanduser("~/.doll/") + config['db_file'])

    create_type_contents()

    parse_inflect_file(inflect_file=words_dir + 'INFLECTS.LAT', commit_changes=commit_changes)

    parse_dict_file(dict_file=words_dir + 'DICTLINE.GEN', commit_changes=commit_changes)
