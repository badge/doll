from doll.db import Connection
from doll.db.model import *
import re
from tqdm import tqdm


class Parser:
    _regex = re.compile('\s([A-Z]):')

    def __init__(self, session):
        self.session = session
        self._word_areas = {word_area.code: word_area for word_area in session.query(WordArea).all()}

    def parse_translation(self, language, entry, translation):
        """Parses the translation line and creates the Translation and TranslationSet objects

        :param language
        :param entry
        :param translation
        """

        for ts in [ts for ts in map(str.strip, translation.split(';')) if len(ts) > 0]:

            # Check if the translation set includes an area
            area_regex = __class__._regex.match(ts)
            if area_regex is not None:
                area = self._word_areas[area_regex.group(0)]
                translation_set = TranslationSet(entry=entry,
                                                 area=area,
                                                 language=language)
            else:
                translation_set = TranslationSet(entry=entry,
                                                 language=language)

            self.session.add(translation_set)

            for t in [t for t in map(str.strip, ts.split(',')) if len(t) > 0]:
                self.session.add(Translation(translation_set=translation_set, translation=t))

    @staticmethod
    def verb_real_conjugation(present_stem: str, conjugation_code: str, variant: int) -> int:
        """Calculates the 'real' conjugation of a verb from its present stem, conjugation
        code, and variant number

        :param present_stem
        :param conjugation_code
        :param variant
        """

        cc = int(conjugation_code)

        if cc in [1, 2]:  # First and second are the same
            return conjugation_code
        elif (cc, variant) == (3, 4):  # Third conjugation, fourth variant is actually fourth
            return 4
        elif cc == 3 and present_stem[-1:] == 'i':  # Third -io
            return 5
        elif cc == 3:  # Other third conjugation verbs
            return 3
        else:
            return cc + 1


def parse_dict_file(dict_file: str, commit_changes: bool = False):
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

    parser = Parser(session=session)

    language = session.query(Language).filter(Language.code == 'E').first()

    print('Parsing dictionary file')

    # Open the dictionary file and loop over its lines
    with open(dict_file, encoding='windows_1252') as f:
        # Start by counting the lines in the file
        line_count = sum(1 for line in f)
        f.seek(0)

        for line in tqdm(f, total=line_count):

            # Create the list of stems, ignoring those that are empty or zzz
            stems = [Stem(stem_number=i, stem_word=s, stem_simple_word=s)
                     for i, s in enumerate([line[i:i + 18].strip() for i in range(0, 58, 19)], 1)
                     if len(s) > 0 and s != 'zzz']

            part_of_speech_code, part_of_speech_data = line[76:82].strip(), [p.strip()
                                                                             for p in line[83:99].split()]

            # Split 100:101, ..., 108:109
            age_code, area_code, location_code, frequency_code, source_code = [line[i]
                                                                               for i in range(100, 109, 2)]
            translation = line[110:].strip()

            # Create the basic entry, i.e. everything except the part of speech data
            entry = Entry(part_of_speech_code=part_of_speech_code,
                          age_code=age_code,
                          area_code=area_code,
                          location_code=location_code,
                          frequency_code=frequency_code,
                          source_code=source_code,
                          translation=translation,
                          stems=stems)

            parser.parse_translation(language=language,
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
                verb_entry.realconjugation_code = Parser.verb_real_conjugation(stems[0].stem_word,
                                                                               verb_entry.conjugation_code,
                                                                               verb_entry.variant)
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
            print('Committing changes to database')
            session.commit()