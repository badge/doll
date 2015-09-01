__author__ = 'Matthew Badger'

from doll.db import Connection
from doll.db.model import *
import re


def parse_translation(session, language, entry, translation):
    """Parses the translation line and creates the Translation and TranslationSet objects"""

    for ts in [ts for ts in map(str.strip, translation.split(';')) if len(ts) > 0]:

        # Check if the translation set includes an area
        area_regex = re.match('\s([A-Z]):', ts)
        if area_regex is not None:
            area = session.query(WordArea).filter(WordArea.code == area_regex.group(0)).first()
            translation_set = TranslationSet(entry=entry,
                                             area=area,
                                             language=language)
        else:
            translation_set = TranslationSet(entry=entry,
                                             language=language)

        session.add(translation_set)

        for t in [t for t in map(str.strip, ts.split(',')) if len(t) > 0]:
            session.add(Translation(translation_set=translation_set,
                                    translation=t))


def parse_dict_file(dict_file, commit_changes=False):

    """Parses a given dictionary file.

    The DICTLINE.GEN file is arranged in rows as follows:
    - 4 x 19 characters of stems
    - 7 characters of PartOfSpeech
    - 17 characters of part-specific info
    - 10 characters covering:
        - Age
        - Area
        - Location
        - Frequency
        - Source

    :param dict_file: The path of the DICTLINE.GEN file
    :param commit_changes: Whether to save changes to the database
    :return: void
    """
    
    session = Connection.session

    # Open the dictionary file and loop over its lines
    with open(dict_file) as f:
        for line in f:
            stem_list = [line[:18].strip(),
                         line[19:37].strip(),
                         line[38:56].strip(),
                         line[57:75].strip()]

            part_of_speech_code = line[76:82].strip()
            part_of_speech_data = line[83:99].strip().split()

            age_code = line[100:101].strip()
            area_code = line[102:103].strip()
            location_code = line[104:105].strip()
            frequency_code = line[106:107].strip()
            source_code = line[108:109].strip()

            translation = line[110:].strip()

            language = session.query(Language).filter(Language.code == 'E').first()

            # Create the list of stems, ignoring those that are empty or zzz
            stems = [Stem(stem_number=i, stem_word=s) for i, s in enumerate(stem_list, 1) if len(s) > 0 and s != 'zzz']

            # Create the basic entry, i.e. everything except the part of speech data
            entry = Entry(part_of_speech_code=part_of_speech_code,
                          age_code=age_code,
                          area_code=area_code,
                          location_code=location_code,
                          frequency_code=frequency_code,
                          source_code=source_code,
                          translation=translation,
                          stems=stems)

            parse_translation(session=session,
                              language=language,
                              entry=entry,
                              translation=translation)

            # Create the specific entry given the part of speech
            if entry.part_of_speech_code == 'N':
                noun_entry = NounEntry(declension_code=part_of_speech_data[0],
                                       variant=int(part_of_speech_data[1]),
                                       gender_code=part_of_speech_data[2],
                                       noun_kind_code=part_of_speech_data[3],
                                       entry=entry)
                session.add(noun_entry)
            elif entry.part_of_speech_code == 'PRON':
                pronoun_entry = PronounEntry(declension_code=part_of_speech_data[0],
                                             variant=int(part_of_speech_data[1]),
                                             pronoun_kind_code=part_of_speech_data[2],
                                             entry=entry)
                session.add(pronoun_entry)
            elif entry.part_of_speech_code == 'PACK':
                propack_entry = PropackEntry(declension_code=part_of_speech_data[0],
                                             variant=int(part_of_speech_data[1]),
                                             pronoun_kind_code=part_of_speech_data[2],
                                             entry=entry)
                session.add(propack_entry)
            elif entry.part_of_speech_code == 'ADJ':
                adjective_entry = AdjectiveEntry(declension_code=part_of_speech_data[0],
                                                 variant=int(part_of_speech_data[1]),
                                                 comparison_type_code=part_of_speech_data[2],
                                                 entry=entry)
                session.add(adjective_entry)
            elif entry.part_of_speech_code == 'NUM':
                numeral_entry = NumeralEntry(declension_code=part_of_speech_data[0],
                                             variant=int(part_of_speech_data[1]),
                                             numeral_sort_code=part_of_speech_data[2],
                                             numeral_value_type=part_of_speech_data[3],
                                             entry=entry)
                session.add(numeral_entry)
            elif entry.part_of_speech_code == 'ADV':
                adverb_entry = AdverbEntry(comparison_type_code=part_of_speech_data[0],
                                           entry=entry)
                session.add(adverb_entry)
            elif entry.part_of_speech_code == 'V':
                verb_entry = VerbEntry(conjugation_code=part_of_speech_data[0],
                                       variant=int(part_of_speech_data[1]),
                                       verb_kind_code=part_of_speech_data[2],
                                       entry=entry)
                session.add(verb_entry)
            elif entry.part_of_speech_code == 'PREP':
                preposition_entry = PrepositionEntry(case_code=part_of_speech_data[0],
                                                     entry=entry)
                session.add(preposition_entry)
            elif entry.part_of_speech_code == 'CONJ':
                conjunction_entry = ConjunctionEntry(entry=entry)
                session.add(conjunction_entry)
            elif entry.part_of_speech_code == 'INTERJ':
                interjection_entry = InterjectionEntry(entry=entry)
                session.add(interjection_entry)

        # If we don't want to commit changes, just list the output
        if not commit_changes:
            session.query(NounEntry).all()
            session.query(PronounEntry).all()
            session.query(PropackEntry).all()
            session.query(AdjectiveEntry).all()
            session.query(NumeralEntry).all()
            session.query(AdverbEntry).all()
            session.query(VerbEntry).all()
            session.query(PrepositionEntry).all()
            session.query(ConjunctionEntry).all()
            session.query(InterjectionEntry).all()
        else:
            session.commit()