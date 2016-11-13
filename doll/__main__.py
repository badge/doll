import doll.data
import doll.input_parser
import doll.parse_test
import argparse

description = """
DDDDDDDDDDDDD                         LLLLLLLLLL        LLLLLLLLLL
D::::::::::::DDD                      L::::::::L        L::::::::L
D:::::::::::::::DD                    L::::::::L        L::::::::L
DDD:::::DDDDD:::::D                   LL::::::LL        LL::::::LL
  D:::::D    D:::::D    ooooooooooo     L::::L            L::::L
  D:::::D     D:::::D oo:::::::::::oo   L::::L            L::::L
  D:::::D     D:::::Do:::::::::::::::o  L::::L            L::::L
  D:::::D     D:::::Do:::::ooooo:::::o  L::::L            L::::L
  D:::::D     D:::::Do::::o     o::::o  L::::L            L::::L
  D:::::D     D:::::Do::::o     o::::o  L::::L            L::::L
  D:::::D     D:::::Do::::o     o::::o  L::::L            L::::L
  D:::::D    D:::::D o::::o     o::::o  L::::L      LLLL  L::::L      LLLL
DDD:::::DDDDD:::::D  o:::::ooooo:::::oLL::::::LLLLLL:::LLL::::::LLLLLL:::L
D:::::::::::::::DD   o:::::::::::::::oL::::::::::::::::LL::::::::::::::::L
D::::::::::::DDD      oo:::::::::::oo L::::::::::::::::LL::::::::::::::::L
DDDDDDDDDDDDD           ooooooooooo   LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL

The Database of Latin Lexicon

An implementation of William Whitaker\'s Words\' data model in Python.

This program comprises three parts:
    - Downloader, to download the Words source files, contained in the 'data'
      module
    - Model, the sqlalchemy model of the data, contained in the 'db' module
    - Parser, which ingests the Words source files and populates the database
      with them, via the sqlalchemy model. This is contained in the
      input_parser module.

In addition, there is a parse_test script in the root directory,
demonstrating a use of the package to replicate certain functionality
of Words.
"""

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-f", "--force", action='store_true', help="Force a re-download of the words.zip file")
    parser.add_argument("-b", "--build", action='store_true', help="Build the database")
    parser.add_argument("-p", "--parse", action='store_true', help="Run the example parser")

    args = parser.parse_args()

    if args.force:
        doll.data.download(create_dir=True)
    if args.build:
        doll.input_parser.parse_all_inputs(commit_changes=True)
    if args.parse:
        while True:
            word = input('Enter a word to parse or type quit() to exit:\n=> ')
            if word == 'quit()':
                break
            doll.parse_test.parse_word(word)
