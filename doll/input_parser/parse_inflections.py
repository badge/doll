from doll.db import Connection
from doll.db.model import *
from tqdm import tqdm

"""Parses the inflections input file.

   This package parses the inflections file and inserts
   its contents to the database. Type tables must
   be populated before this is run.

"""


def parse_inflect_file(inflect_file, commit_changes=False):
    session = Connection.session

    # Dictionary to define the start of the line
    line_start = {
        'N': 6,
        'PRON': 6,
        'ADJ': 7,
        'NUM': 7,
        'ADV': 2,
        'V': 8,
        'VPAR': 9,
        'SUPINE': 6,
        'PREP': 2,
        'CONJ': 1,
        'INTERJ': 1
    }

    print('Parsing inflections file')

    # Open the inflections file and loop over its lines
    with open(inflect_file, encoding='windows_1252') as f:
        # Start by counting the lines in the file
        line_count = sum(1 for line in f)
        f.seek(0)

        for line in tqdm(f, total=line_count):
            line_split = line.split()
            if len(line_split) > 0 and line_split[0][0] != '-':
                i = line_start[line_split[0]]
                # Check if we have an empty record
                if len(line_split[i + 2]) == 1 and line_split[i + 2] == line_split[i + 2].upper():
                    i -= 1
                    ending = ''
                else:
                    ending = line_split[i + 2]
                if line_split[0] == 'N':
                    noun = NounRecord(
                        declension_code=line_split[1],
                        variant=line_split[2],
                        case_code=line_split[3],
                        number_code=line_split[4],
                        gender_code=line_split[5],
                        record=Record(
                            part_of_speech_code=line_split[0],
                            stem_key=line_split[i],
                            ending=ending,
                            age_code=line_split[i + 3],
                            frequency_code=line_split[i + 4],
                            notes=" ".join(line_split[i + 6:])
                        ))
                    session.add(noun)
                elif line_split[0] == 'ADJ':
                    adjective = AdjectiveRecord(
                        declension_code=line_split[1],
                        variant=line_split[2],
                        case_code=line_split[3],
                        number_code=line_split[4],
                        gender_code=line_split[5],
                        comparison_type_code=line_split[6],
                        record=Record(
                            part_of_speech_code=line_split[0],
                            stem_key=line_split[i],
                            ending=ending,
                            age_code=line_split[i + 3],
                            frequency_code=line_split[i + 4],
                            notes=" ".join(line_split[i + 6:])
                        ))
                    session.add(adjective)
                elif line_split[0] == 'PRON':
                    pronoun = PronounRecord(
                        declension_code=line_split[1],
                        variant=line_split[2],
                        case_code=line_split[3],
                        number_code=line_split[4],
                        gender_code=line_split[5],
                        record=Record(
                            part_of_speech_code=line_split[0],
                            stem_key=line_split[i],
                            ending=ending,
                            age_code=line_split[i + 3],
                            frequency_code=line_split[i + 4],
                            notes=" ".join(line_split[i + 6:])
                        ))
                    session.add(pronoun)
                elif line_split[0] == 'NUM':
                    numeral = NumeralRecord(
                        declension_code=line_split[1],
                        variant=line_split[2],
                        case_code=line_split[3],
                        number_code=line_split[4],
                        gender_code=line_split[5],
                        numeral_sort_code=line_split[6],
                        record=Record(
                            part_of_speech_code=line_split[0],
                            stem_key=line_split[i],
                            ending=ending,
                            age_code=line_split[i + 3],
                            frequency_code=line_split[i + 4],
                            notes=" ".join(line_split[i + 6:])
                        ))
                    session.add(numeral)
                elif line_split[0] == 'V':
                    verb = VerbRecord(
                        conjugation_code=line_split[1],
                        variant=line_split[2],
                        tense_code=line_split[3],
                        voice_code=line_split[4],
                        mood_code=line_split[5],
                        person_code=line_split[6],
                        number_code=line_split[7],
                        record=Record(
                            part_of_speech_code=line_split[0],
                            stem_key=line_split[i],
                            ending=ending,
                            age_code=line_split[i + 3],
                            frequency_code=line_split[i + 4],
                            notes=" ".join(line_split[i + 6:])
                        ))
                    session.add(verb)
                elif line_split[0] == 'VPAR':
                    verbparticiple = VerbParticipleRecord(
                        conjugation_code=line_split[1],
                        variant=line_split[2],
                        case_code=line_split[3],
                        number_code=line_split[4],
                        gender_code=line_split[5],
                        tense_code=line_split[6],
                        voice_code=line_split[7],
                        mood_code=line_split[8],
                        record=Record(
                            part_of_speech_code=line_split[0],
                            stem_key=line_split[i],
                            ending=ending,
                            age_code=line_split[i + 3],
                            frequency_code=line_split[i + 4],
                            notes=" ".join(line_split[i + 6:])
                        ))
                    session.add(verbparticiple)
                elif line_split[0] == 'SUPINE':
                    supine = SupineRecord(
                        conjugation_code=line_split[1],
                        variant=line_split[2],
                        case_code=line_split[3],
                        number_code=line_split[4],
                        gender_code=line_split[5],
                        record=Record(
                            part_of_speech_code=line_split[0],
                            stem_key=line_split[i],
                            ending=ending,
                            age_code=line_split[i + 3],
                            frequency_code=line_split[i + 4],
                            notes=" ".join(line_split[i + 6:])
                        ))
                    session.add(supine)

                # None of the remaining types have an ending, so we don't need to check
                elif line_split[0] == 'ADV':
                    adverb = AdverbRecord(
                        comparison_type_code=line_split[1],
                        record=Record(
                            part_of_speech_code=line_split[0],
                            stem_key=line_split[i],
                            ending='',
                            age_code=line_split[i + 2],
                            frequency_code=line_split[i + 3],
                            notes=" ".join(line_split[i + 5:])
                        ))
                    session.add(adverb)
                elif line_split[0] == 'PREP':
                    preposition = PrepositionRecord(
                        case_code=line_split[1],
                        record=Record(
                            part_of_speech_code=line_split[0],
                            stem_key=line_split[i],
                            ending='',
                            age_code=line_split[i + 2],
                            frequency_code=line_split[i + 3],
                            notes=" ".join(line_split[i + 5:])
                        ))
                    session.add(preposition)
                elif line_split[0] == 'CONJ':
                    conjunction = ConjunctionRecord(
                        record=Record(
                            part_of_speech_code=line_split[0],
                            stem_key=line_split[i],
                            ending='',
                            age_code=line_split[i + 2],
                            frequency_code=line_split[i + 3],
                            notes=" ".join(line_split[i + 5:])
                        ))
                    session.add(conjunction)
                elif line_split[0] == 'INTERJ':
                    interjection = InterjectionRecord(
                        record=Record(
                            part_of_speech_code=line_split[0],
                            stem_key=line_split[i],
                            ending='',
                            age_code=line_split[i + 2],
                            frequency_code=line_split[i + 3],
                            notes=" ".join(line_split[i + 5:])
                        ))
                    session.add(interjection)

    if commit_changes:
        session.commit()
    else:
        session.query(NounRecord).all()
        session.query(AdjectiveRecord).all()
        session.query(PronounRecord).all()
        session.query(NumeralRecord).all()
        session.query(VerbRecord).all()
        session.query(VerbParticipleRecord).all()
        session.query(AdverbRecord).all()
        session.query(PrepositionRecord).all()
        session.query(ConjunctionRecord).all()
        session.query(InterjectionRecord).all()
        session.query(SupineRecord).all()