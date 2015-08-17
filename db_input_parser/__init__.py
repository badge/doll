__author__ = 'Matthew'


from db_input_parser.add_database_types import create_type_contents
from db_input_parser.parse_dictionary import parse_dict_file
from db_input_parser.parse_inflections import parse_inflect_file


def parse_all_inputs(words_folder, commit_changes):
    """Creates the database and parses all the inputs"""

    create_type_contents()

    parse_inflect_file(inflect_file=words_folder + 'INFLECTS.LAT', commit_changes=commit_changes)

    parse_dict_file(dict_file=words_folder + 'DICTLINE.GEN', commit_changes=commit_changes)

