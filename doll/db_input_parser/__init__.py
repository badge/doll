__author__ = 'Matthew'

import os

from db_input_parser.add_database_types import create_type_contents
from db_input_parser.parse_dictionary import parse_dict_file
from doll.db_input_parser.parse_inflections import parse_inflect_file


def parse_all_inputs(words_folder, commit_changes):
    """Creates the database and parses all the inputs"""

    # Add a trailing slash if necessary
    if (words_folder[-1:] != '/'):
        words_folder += '/'

    # First check that our words folder exists
    if not os.path.isdir(words_folder):
        print('Cannot find words_folder at {0}! Exiting...'.format(words_folder))
        return

    # And then that our input files exist
    files_to_find = ['INFLECTS.LAT', 'DICTLINE.GEN']
    error_string = ', '.join([f for f in files_to_find if not os.path.isfile(words_folder + f)])

    if not error_string == '':
        print('Unable to find the following file(s): ' + error_string + '. Exiting...')
        return

    '''if os.path.isfile(config['db_file']):
        if not input('Database file exists, overwrite? ([Y]es/ No)')[:1] == 'Y':
            print('Database file exists, exiting...')
            return'''

    create_type_contents()

    parse_inflect_file(inflect_file=words_folder + 'INFLECTS.LAT', commit_changes=commit_changes)

    parse_dict_file(dict_file=words_folder + 'DICTLINE.GEN', commit_changes=commit_changes)

