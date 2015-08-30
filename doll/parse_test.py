__author__ = 'Matthew Badger'

from sqlalchemy import func, or_, and_

from doll.db import *

session = Connection.session


def parse_word(word):
    # Possible entries are those where the stem joined to its appropriate endings
    # create our input word.
    possible_entries = [(e, r, s) for e, r, s in session.query(Entry, Record, Stem)
        .filter(and_(Record.part_of_speech_code == Entry.part_of_speech_code,
                     Record.stem_key == Stem.stem_number))
        .filter(Stem.entry_id == Entry.id)
        .filter(func.substr(word, 1, func.length(Stem.stem_word)) == Stem.stem_word)
        .filter(Stem.stem_word + Record.ending == word)]

    # It would be preferable to get a list of possible records based on
    # the possible entries, then filter further by word type, however
    # it is quicker simply to deal with each entry as a whole.
    for (entry, record, stem) in possible_entries:
        if entry.part_of_speech_code == 'N':
            for noun_record in session.query(NounRecord) \
                    .join(NounEntry, and_(NounRecord.declension_code == NounEntry.declension_code,
                                          or_(NounRecord.variant == NounEntry.variant,
                                              NounRecord.variant == 0),
                                          or_(NounRecord.gender_code == NounEntry.gender_code,
                                              and_(NounRecord.gender_code == 'C',
                                                   NounEntry.gender_code.in_(('F', 'M'))),
                                              NounRecord.gender_code == 'X'))) \
                    .filter(NounRecord.record_id == record.id) \
                    .filter(Record.stem_key == stem.stem_number) \
                    .filter(NounEntry.entry_id == entry.id) \
                    .all():
                print('{0} - {1} Declension, {2} {3} - {4}'.format(
                    stem.stem_word + '.' + noun_record.record.ending,
                    noun_record.declension.name,
                    noun_record.case.name,
                    noun_record.number.name,
                    entry.translation))
        elif entry.part_of_speech_code == 'V':
            for verb_record in session.query(VerbRecord) \
                    .join(VerbEntry, and_(VerbRecord.conjugation_code == VerbEntry.conjugation_code,
                                          or_(VerbRecord.variant == VerbEntry.variant,
                                              VerbEntry.variant == 0))) \
                    .filter(VerbRecord.record_id == record.id) \
                    .filter(Record.stem_key == stem.stem_number) \
                    .filter(VerbEntry.entry_id == entry.id) \
                    .all():
                print('{0} - {1} Conjugation, {2} Person {3} - {4}'.format(
                    stem.stem_word + '.' + verb_record.record.ending,
                    verb_record.conjugation.name,
                    verb_record.person.name,
                    verb_record.number.name,
                    entry.translation))
        elif entry.part_of_speech_code == 'PRON':
            for pronoun_record in session.query(PronounRecord) \
                    .join(PronounEntry, and_(PronounRecord.declension_code == PronounEntry.declension_code,
                                             or_(PronounRecord.variant == PronounEntry.variant,
                                                 PronounRecord.variant == 0))) \
                    .filter(PronounRecord.record_id == record.id) \
                    .filter(Record.stem_key == stem.stem_number) \
                    .filter(PronounEntry.entry_id == entry.id) \
                    .all():
                print('{0} - {1} Declension, {2} {3} - {4}'.format(
                    stem.stem_word + '.' + pronoun_record.record.ending,
                    pronoun_record.declension.name,
                    pronoun_record.case.name,
                    pronoun_record.number.name,
                    entry.translation))
        elif entry.part_of_speech_code == 'ADJ':
            for adjective_record in session.query(AdjectiveRecord) \
                    .join(AdjectiveEntry, and_(AdjectiveRecord.declension_code == AdjectiveEntry.declension_code,
                                               or_(AdjectiveRecord.variant == AdjectiveEntry.variant,
                                                   AdjectiveRecord.variant == 0),
                                               AdjectiveRecord.comparison_type_code == AdjectiveEntry.comparison_type_code)) \
                    .filter(AdjectiveRecord.record_id == record.id) \
                    .filter(Record.stem_key == stem.stem_number) \
                    .filter(AdjectiveEntry.entry_id == entry.id) \
                    .all():
                print('{0} - {1} Declension, {2} {3} ({4}) - {5}'.format(
                    stem.stem_word + '.' + adjective_record.record.ending,
                    adjective_record.declension.name,
                    adjective_record.case.name,
                    adjective_record.number.name,
                    adjective_record.comparison_type.name,
                    entry.translation))


print('Welcome to Words!')
while True:
    word = input('Enter a word to parse or type quit() to exit:\n')
    if word == 'quit()':
        break
    parse_word(word)
