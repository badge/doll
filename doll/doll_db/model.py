"""Defines the model for the database.

This package defines the database model, which is in roughly three parts:

1. Type classes, linked with type_ tables in the database, which define
   the basic elements of other classes, such as word age, or declension.
   In general, these come from the inflections_package.ads file in Words.
2. Record classes, linked with record_ tables in the database, which
   define the inflections for the various word types. These also come
   from the inflections_package.ads file; the data for the records
   themselves in the INFLECTS.LAT file.
3. Dictionary classes, linked with the dictionary_ tables in the database,
   which define the actual word entries. These are defined along the
   lines of the dictionary_package.ads file; their data from the
   DICTLINE.GEN file.

In general, a word type (such as a noun), will have both a record class
(NounRecord), and an dictionary entry class (NounEntry). A dictionary
entry links to a record based on the type elements therein. For a noun,
this means that inflections with the same gender and declension.
        
"""

__author__ = 'Matthew Badger'

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Unicode
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr

from doll.doll_db import Base

"""Basic Type Classes

These classes define the basic types used by all parts of the dictionary,
such as PartOfSpeech (noun, verb, etc.) and Mood. They have a base class
TypeBase, which defines an id, code, name and description.

Most of the type classes define no other columns. The code matches that
in Whitaker's source, and has a unique key. id is just for backrefernces
by sqlalchemy. name is hopefully a better thing to present to the user
than the code.

"""


# Base table object, with id, code, name, and description columns
class TypeBase(object):
    @declared_attr
    def __tablename__(self):
        return 'type_' + self.__name__.lower()

    id = Column(Integer, primary_key=True)
    code = Column(String(10), unique=True)
    name = Column(String(50))
    description = Column(String(300))


class PartOfSpeech(TypeBase, Base):
    """Elements of speech such as a noun. Helper elements used in
    code have is_real False."""

    is_real = Column(Boolean)
    record_start = Column(Integer)


class WordAge(TypeBase, Base):
    """Ages when the word is found"""


class WordFrequency(TypeBase, Base):
    """Frequency of occurrence in the corpus"""


class WordArea(TypeBase, Base):
    """Taxonomic Area"""


class WordLocation(TypeBase, Base):
    """Geographical Area"""


class WordSource(TypeBase, Base):
    """Word Source"""


class Number(TypeBase, Base):
    """Singular or Plural"""


# Noun Type Classes
class Declension(TypeBase, Base):
    """Declensions"""

    order = Column(Integer)

    def __lt__(self, other):
        return self.order < other.order


class Gender(TypeBase, Base):
    """Genders"""


class Case(TypeBase, Base):
    """Cases for nouns"""

    is_default = Column(Boolean)
    uk_order = Column(Integer)
    us_order = Column(Integer)


# Verb Type Classes
class Conjugation(TypeBase, Base):
    """Conjugation"""


class Person(TypeBase, Base):
    """Person - First, Second or Third"""

    order = Column(Integer)

    def __lt__(self, other):
        return self.order < other.order


class Tense(TypeBase, Base):
    """Tense"""


class Voice(TypeBase, Base):
    """Voice"""


class Mood(TypeBase, Base):
    """Mood"""


# Adjective and Adverb Type Classes
class ComparisonType(TypeBase, Base):
    """Adjective comparison types"""


# Numeral Type Classes
class NumeralSort(TypeBase, Base):
    """The type of numeral we have"""


# Word Kind Classes
class NounKind(TypeBase, Base):
    """Kinds of nouns"""


class PronounKind(TypeBase, Base):
    """Kinds of pronouns"""


class VerbKind(TypeBase, Base):
    """Kinds of verbs"""


# Language, not used by Words and currently only contains English
class Language(TypeBase, Base):
    """Languages for translation"""



"""Inflection Record Classes.

These classes define the inflection records, built from
the contents of INFLECTS.LAT. To normalise the data we have
a basic Record class, which details all the information
common to all inflection records. Note that we include the
ending itself, as this is always a string of length >= 0,
and is unique (...obviously). For dictionary records we
won't do this

"""


# Record Base class
class Record(Base):
    """Inflection Record class, with columns shared by all records"""
    __tablename__ = 'inflection_record'

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Foreign Keys
    part_of_speech_code = Column(String(10), ForeignKey('type_partofspeech.code',
                                                        name='FK_inflection_record_part_of_speech_code'))
    age_code = Column(String(10), ForeignKey('type_wordage.code',
                                             name='FK_inflection_record_wordage_code'))
    frequency_code = Column(String(10), ForeignKey('type_wordfrequency.code',
                                                   name='FK_inflection_record_wordfrequency_code'))

    # Other columns
    stem_key = Column(Integer)
    ending = Column(Unicode(20, collation='BINARY'))  # We use binary collation so a is not ā
    notes = Column(Unicode(200, collation='BINARY'))

    # Relationships
    part_of_speech = relationship('PartOfSpeech', backref=backref('inflection_record'))
    age = relationship('WordAge', backref=backref('inflection_record'))
    frequency = relationship('WordFrequency', backref=backref('inflection_record'))


# Noun Record class
class NounRecord(Base):
    """Inflection record for a noun"""
    __tablename__ = 'inflection_noun'

    id = Column(Integer, primary_key=True, autoincrement=True)
    record_id = Column(Integer, ForeignKey('inflection_record.id',
                                           name='FK_inflection_noun_record_id'))

    declension_code = Column(String(10), ForeignKey('type_declension.code',
                                                    name='FK_inflection_noun_declension_code'))
    variant = Column(Integer)
    case_code = Column(String(10), ForeignKey('type_case.code',
                                              name='FK_inflection_noun_case_code'))
    number_code = Column(String(10), ForeignKey('type_number.code',
                                                name='FK_inflection_noun_number_code'))
    gender_code = Column(String(10), ForeignKey('type_gender.code',
                                                name='FK_inflection_noun_gender_code'))

    # Relationships
    record = relationship('Record', backref=backref('inflection_noun'))
    declension = relationship('Declension', backref=backref('inflection_noun'))
    case = relationship('Case', backref=backref('inflection_noun'))
    number = relationship('Number', backref=backref('inflection_noun'))
    gender = relationship('Gender', backref=backref('inflection_noun'))


class PronounRecord(Base):
    """Inflection record for a pronoun"""
    __tablename__ = 'inflection_pronoun'

    id = Column(Integer, primary_key=True, autoincrement=True)
    record_id = Column(Integer, ForeignKey('inflection_record.id',
                                           name='FK_inflection_pronoun_record_id'))

    declension_code = Column(String(10), ForeignKey('type_declension.code',
                                                    name='FK_inflection_pronoun_declension_code'))
    variant = Column(Integer)
    case_code = Column(String(10), ForeignKey('type_case.code',
                                              name='FK_inflection_pronoun_case_code'))
    number_code = Column(String(10), ForeignKey('type_number.code',
                                                name='FK_inflection_pronoun_number_code'))
    gender_code = Column(String(10), ForeignKey('type_gender.code',
                                                name='FK_inflection_pronoun_gender_code'))

    # Relationships
    record = relationship('Record', backref=backref('inflection_pronoun'))
    declension = relationship('Declension', backref=backref('inflection_pronoun'))
    case = relationship('Case', backref=backref('inflection_pronoun'))
    number = relationship('Number', backref=backref('inflection_pronoun'))
    gender = relationship('Gender', backref=backref('inflection_pronoun'))


# Adjective Record class
class AdjectiveRecord(Base):
    """Inflection record for an adjective"""
    __tablename__ = 'inflection_adjective'

    id = Column(Integer, primary_key=True, autoincrement=True)
    record_id = Column(Integer, ForeignKey('inflection_record.id',
                                           name='FK_inflection_adjective_record_id'))

    declension_code = Column(String(10), ForeignKey('type_declension.code',
                                                    name='FK_inflection_adjective_declension_code'))
    variant = Column(Integer)
    case_code = Column(String(10), ForeignKey('type_case.code',
                                              name='FK_inflection_adjective_case_code'))
    number_code = Column(String(10), ForeignKey('type_number.code',
                                                name='FK_inflection_adjective_number_code'))
    gender_code = Column(String(10), ForeignKey('type_gender.code',
                                                name='FK_inflection_adjective_gender_code'))
    comparison_type_code = Column(String(10), ForeignKey('type_comparisontype.code',
                                                         name='FK_inflection_adjective_comparisontype_code'))

    # Relationships
    record = relationship('Record', backref=backref('inflection_adjective'))
    declension = relationship('Declension', backref=backref('inflection_adjective'))
    case = relationship('Case', backref=backref('inflection_adjective'))
    number = relationship('Number', backref=backref('inflection_adjective'))
    gender = relationship('Gender', backref=backref('inflection_adjective'))
    comparison_type = relationship('ComparisonType', backref=backref('inflection_adjective'))


# Numeral Record class
class NumeralRecord(Base):
    """Inflection record for a Numeral"""
    __tablename__ = 'inflection_numeral'

    id = Column(Integer, primary_key=True, autoincrement=True)
    record_id = Column(Integer, ForeignKey('inflection_record.id',
                                           name='FK_inflection_numeral_record_id'))

    declension_code = Column(String(10), ForeignKey('type_declension.code',
                                                    name='FK_inflection_numeral_declension_code'))
    variant = Column(Integer)
    case_code = Column(String(10), ForeignKey('type_case.code',
                                              name='FK_inflection_numeral_case_code'))
    number_code = Column(String(10), ForeignKey('type_number.code',
                                                name='FK_inflection_numeral_number_code'))
    gender_code = Column(String(10), ForeignKey('type_gender.code',
                                                name='FK_inflection_numeral_gender_code'))
    numeral_sort_code = Column(String(10), ForeignKey('type_numeralsort.code',
                                                      name='FK_inflection_numeral_numeralsort_code'))

    # Relationships
    record = relationship('Record', backref=backref('inflection_numeral'))
    declension = relationship('Declension', backref=backref('inflection_numeral'))
    case = relationship('Case', backref=backref('inflection_numeral'))
    number = relationship('Number', backref=backref('inflection_numeral'))
    gender = relationship('Gender', backref=backref('inflection_numeral'))
    numeral_sort = relationship('NumeralSort', backref=backref('inflection_numeral'))


# Verb Record class
class VerbRecord(Base):
    """Inflection record for a verb"""
    __tablename__ = 'inflection_verb'

    id = Column(Integer, primary_key=True, autoincrement=True)
    record_id = Column(Integer, ForeignKey('inflection_record.id',
                                           name='FK_inflection_verb_record_id'))

    conjugation_code = Column(String(10), ForeignKey('type_conjugation.code',
                                                     name='FK_inflection_verb_conjugation_code'))
    variant = Column(Integer)

    tense_code = Column(String(10), ForeignKey('type_tense.code',
                                               name='FK_inflection_verb_tense_code'))
    voice_code = Column(String(10), ForeignKey('type_voice.code',
                                               name='FK_inflection_verb_voice_code'))
    mood_code = Column(String(10), ForeignKey('type_mood.code',
                                              name='FK_inflection_verb_mood_code'))
    person_code = Column(String(10), ForeignKey('type_person.code',
                                                name='FK_inflection_verb_person_code'))
    number_code = Column(String(10), ForeignKey('type_number.code',
                                                name='FK_inflection_verb_number_code'))

    # Relationships
    record = relationship('Record', backref=backref('inflection_verb'))
    conjugation = relationship('Conjugation', backref=backref('inflection_verb'))
    tense = relationship('Tense', backref=backref('inflection_verb'))
    voice = relationship('Voice', backref=backref('inflection_verb'))
    mood = relationship('Mood', backref=backref('inflection_verb'))
    person = relationship('Person', backref=backref('inflection_verb'))
    number = relationship('Number', backref=backref('inflection_verb'))


# Verb Record class
class VerbParticipleRecord(Base):
    """Inflection record for a Verb Participle"""
    __tablename__ = 'inflection_verbparticiple'

    id = Column(Integer, primary_key=True, autoincrement=True)
    record_id = Column(Integer, ForeignKey('inflection_record.id',
                                           name='FK_inflection_verbparticiple_record_id'))

    conjugation_code = Column(String(10), ForeignKey('type_conjugation.code',
                                                     name='FK_inflection_verbparticiple_conjugation_code'))
    variant = Column(Integer)
    case_code = Column(String(10), ForeignKey('type_case.code',
                                              name='FK_inflection_verbparticiple_case_code'))
    number_code = Column(String(10), ForeignKey('type_number.code',
                                                name='FK_inflection_verbparticiple_number_code'))
    gender_code = Column(String(10), ForeignKey('type_gender.code',
                                                name='FK_inflection_verbparticiple_gender_code'))
    tense_code = Column(String(10), ForeignKey('type_tense.code',
                                               name='FK_inflection_verbparticiple_tense_code'))
    voice_code = Column(String(10), ForeignKey('type_voice.code',
                                               name='FK_inflection_verbparticiple_voice_code'))
    mood_code = Column(String(10), ForeignKey('type_mood.code',
                                              name='FK_inflection_verbparticiple_mood_code'))

    # Relationships
    record = relationship('Record', backref=backref('inflection_verbparticiple'))
    conjugation = relationship('Conjugation', backref=backref('inflection_verbparticiple'))
    number = relationship('Number', backref=backref('inflection_verbparticiple'))
    gender = relationship('Gender', backref=backref('inflection_verbparticiple'))
    tense = relationship('Tense', backref=backref('inflection_verbparticiple'))
    voice = relationship('Voice', backref=backref('inflection_verbparticiple'))
    mood = relationship('Mood', backref=backref('inflection_verbparticiple'))


class AdverbRecord(Base):
    """Inflection record for an Adverb"""
    __tablename__ = 'inflection_adverb'

    id = Column(Integer, primary_key=True, autoincrement=True)
    record_id = Column(Integer, ForeignKey('inflection_record.id',
                                           name='FK_inflection_adverb_record_id'))
    comparison_type_code = Column(String(10), ForeignKey('type_comparisontype.code',
                                                         name='FK_inflection_adverb_comparisontype_code'))

    # Relationships
    record = relationship('Record', backref=backref('inflection_adverb'))
    comparison_type = relationship('ComparisonType', backref=backref('inflection_adverb'))


class PrepositionRecord(Base):
    """Inflection record for a Preposition"""
    __tablename__ = 'inflection_preposition'

    id = Column(Integer, primary_key=True, autoincrement=True)
    record_id = Column(Integer, ForeignKey('inflection_record.id',
                                           name='FK_inflection_preposition_record_id'))
    case_code = Column(String(10), ForeignKey('type_case.code',
                                              name='FK_inflection_preposition_case_code'))

    # Relationships
    record = relationship('Record', backref=backref('inflection_preposition'))
    case = relationship('Case', backref=backref('inflection_preposition'))


class ConjunctionRecord(Base):
    """Inflection record for a Conjunction"""
    __tablename__ = 'inflection_conjunction'

    id = Column(Integer, primary_key=True, autoincrement=True)
    record_id = Column(Integer, ForeignKey('inflection_record.id',
                                           name='FK_inflection_conjunction_record_id'))

    # Relationships
    record = relationship('Record', backref=backref('inflection_conjunction'))


class InterjectionRecord(Base):
    """Inflection record for a Interjection"""
    __tablename__ = 'inflection_interjection'

    id = Column(Integer, primary_key=True, autoincrement=True)
    record_id = Column(Integer, ForeignKey('inflection_record.id',
                                           name='FK_inflection_interjection_record_id'))

    # Relationships
    record = relationship('Record', backref=backref('inflection_interjection'))


class SupineRecord(Base):
    """Inflection record for a Supine"""
    __tablename__ = 'inflection_supine'

    id = Column(Integer, primary_key=True, autoincrement=True)
    record_id = Column(Integer, ForeignKey('inflection_record.id',
                                           name='FK_inflection_supine_record_id'))

    conjugation_code = Column(String(10), ForeignKey('type_conjugation.code',
                                                     name='FK_inflection_supine_conjugation_code'))
    variant = Column(Integer)
    case_code = Column(String(10), ForeignKey('type_case.code',
                                              name='FK_inflection_supine_case_code'))
    number_code = Column(String(10), ForeignKey('type_number.code',
                                                name='FK_inflection_supine_number_code'))
    gender_code = Column(String(10), ForeignKey('type_gender.code',
                                                name='FK_inflection_supine_gender_code'))

    # Relationships
    record = relationship('Record', backref=backref('inflection_supine'))
    conjugation = relationship('Conjugation', backref=backref('inflection_supine'))
    case = relationship('Case', backref=backref('inflection_supine'))
    number = relationship('Number', backref=backref('inflection_supine'))
    gender = relationship('Gender', backref=backref('inflection_supine'))


"""Dictionary Entries classes.

   
"""


class Entry(Base):
    """Basic dictionary entry class"""
    __tablename__ = 'dictionary_entry'

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Foreign Keys
    part_of_speech_code = Column(String(10), ForeignKey('type_partofspeech.code',
                                                        name='FK_dictionary_entry_part_of_speech_code'))
    age_code = Column(String(10), ForeignKey('type_wordage.code',
                                             name='FK_dictionary_entry_wordage_code'))
    area_code = Column(String(10), ForeignKey('type_wordarea.code',
                                              name='FK_dictionary_entry_wordarea_code'))
    location_code = Column(String(10), ForeignKey('type_wordlocation.code',
                                                  name='FK_dictionary_entry_wordlocation_code'))
    frequency_code = Column(String(10), ForeignKey('type_wordfrequency.code',
                                                   name='FK_dictionary_entry_wordfrequency_code'))
    source_code = Column(String(10), ForeignKey('type_wordsource.code',
                                                name='FK_dictionary_entry_wordsource_code'))

    translation = Column(Unicode(4096, collation='BINARY'))

    # Relationships
    part_of_speech = relationship('PartOfSpeech', backref=backref('dictionary_entry'))
    age = relationship('WordAge', backref=backref('dictionary_entry'))
    area = relationship('WordArea', backref=backref('dictionary_entry'))
    location = relationship('WordLocation', backref=backref('dictionary_entry'))
    frequency = relationship('WordFrequency', backref=backref('dictionary_entry'))
    source = relationship('WordSource', backref=backref('dictionary_entry'))

    stems = relationship('Stem', backref=backref('dictionary_stem'))


# Stem of a dictionary entry
class Stem(Base):
    """Stem from the Dictionary"""
    __tablename__ = 'dictionary_stem'

    id = Column(Integer, primary_key=True, autoincrement=True)

    entry_id = Column(Integer, ForeignKey('dictionary_entry.id',
                                          name='FK_dictionary_stem_entry_id'))

    stem_number = Column(Integer)
    stem_word = Column(Unicode(20, collation='BINARY'))  # We use binary collation so a is not ā

    # Relationships
    entry = relationship('Entry', backref=backref('dictionary_stem'))



'''

Start of a translation model, but we need groups...

# Translation
class Translation(Base):
    """A translation of a word in a given language"""
    __tablename__ = 'dictionary_translation'

    id = Column(Integer, primary_key=True, autoincrement=True)

    entry_id = Column(Integer, ForeignKey('dictionary_entry.id',
                                          name='FK_dictionary_translation_entry_id'))

    language_id = Column(Integer, ForeignKey('type_language.id',
                                          name='FK_dictionary_translation_language_id'))

    # Relationships
    entry = relationship('Entry', backref=backref('dictionary_translation'))
    language = relationship('Language', backref=backref('dictionary_translation'))
'''


# Noun Entry
class NounEntry(Base):
    """Noun entry in the dictionary"""
    __tablename__ = 'dictionary_noun'

    id = Column(Integer, primary_key=True, autoincrement=True)

    entry_id = Column(Integer, ForeignKey('dictionary_entry.id',
                                          name='FK_dictionary_noun_entry_id'))

    declension_code = Column(String(10), ForeignKey('type_declension.code',
                                                    name='FK_dictionary_noun_declension_code'))
    variant = Column(Integer)
    gender_code = Column(String(10), ForeignKey('type_gender.code',
                                                name='FK_dictionary_noun_gender_code'))
    noun_kind_code = Column(String(10), ForeignKey('type_nounkind.code',
                                                   name='FK_dictionary_noun_nounkind_code'))

    # Relationships
    entry = relationship('Entry', backref=backref('dictionary_noun'))
    declension = relationship('Declension', backref=backref('dictionary_noun'))
    gender = relationship('Gender', backref=backref('dictionary_noun'))
    noun_kind = relationship('NounKind', backref=backref('dictionary_noun'))


# Pronoun Entry
class PronounEntry(Base):
    """Pronoun entry in the dictionary"""
    __tablename__ = 'dictionary_pronoun'

    id = Column(Integer, primary_key=True, autoincrement=True)

    entry_id = Column(Integer, ForeignKey('dictionary_entry.id',
                                          name='FK_dictionary_pronoun_entry_id'))

    declension_code = Column(String(10), ForeignKey('type_declension.code',
                                                    name='FK_dictionary_pronoun_declension_code'))
    variant = Column(Integer)
    pronoun_kind_code = Column(String(10), ForeignKey('type_pronounkind.code',
                                                      name='FK_dictionary_pronoun_pronounkind_code'))

    # Relationships
    entry = relationship('Entry', backref=backref('dictionary_pronoun'))
    declension = relationship('Declension', backref=backref('dictionary_pronoun'))
    pronoun_kind = relationship('PronounKind', backref=backref('dictionary_pronoun'))


# Propack Entry
class PropackEntry(Base):
    """Propack entry in the dictionary"""
    __tablename__ = 'dictionary_propack'

    id = Column(Integer, primary_key=True, autoincrement=True)

    entry_id = Column(Integer, ForeignKey('dictionary_entry.id',
                                          name='FK_dictionary_propack_entry_id'))

    declension_code = Column(String(10), ForeignKey('type_declension.code',
                                                    name='FK_dictionary_propack_declension_code'))
    variant = Column(Integer)
    pronoun_kind_code = Column(String(10), ForeignKey('type_pronounkind.code',
                                                      name='FK_dictionary_propack_pronounkind_code'))

    # Relationships
    entry = relationship('Entry', backref=backref('dictionary_propack'))
    declension = relationship('Declension', backref=backref('dictionary_propack'))
    pronoun_kind = relationship('PronounKind', backref=backref('dictionary_propack'))


# Adjective Entry
class AdjectiveEntry(Base):
    """Adjective entry in the dictionary"""
    __tablename__ = 'dictionary_adjective'

    id = Column(Integer, primary_key=True, autoincrement=True)

    entry_id = Column(Integer, ForeignKey('dictionary_entry.id',
                                          name='FK_dictionary_adjective_entry_id'))

    declension_code = Column(String(10), ForeignKey('type_declension.code',
                                                    name='FK_dictionary_adjective_declension_code'))
    variant = Column(Integer)
    comparison_type_code = Column(String(10), ForeignKey('type_comparisontype.code',
                                                         name='FK_dictionary_adjective_comparisontype_code'))

    # Relationships
    entry = relationship('Entry', backref=backref('dictionary_adjective'))
    declension = relationship('Declension', backref=backref('dictionary_adjective'))
    comparison_type = relationship('ComparisonType', backref=backref('dictionary_adjective'))


# Numeral Entry
class NumeralEntry(Base):
    """Numeral entry in the dictionary"""
    __tablename__ = 'dictionary_numeral'

    id = Column(Integer, primary_key=True, autoincrement=True)

    entry_id = Column(Integer, ForeignKey('dictionary_entry.id',
                                          name='FK_dictionary_numeral_entry_id'))

    declension_code = Column(String(10), ForeignKey('type_declension.code',
                                                    name='FK_dictionary_numeral_declension_code'))
    variant = Column(Integer)
    numeral_sort_code = Column(String(10), ForeignKey('type_numeralsort.code',
                                                      name='FK_dictionary_numeral_numeralsort_code'))
    numeral_value_type = Column(Integer)

    # Relationships
    entry = relationship('Entry', backref=backref('dictionary_numeral'))
    declension = relationship('Declension', backref=backref('dictionary_numeral'))
    numeral_sort = relationship('NumeralSort', backref=backref('dictionary_numeral'))


# Adverb Entry
class AdverbEntry(Base):
    """Adverb entry in the dictionary"""
    __tablename__ = 'dictionary_adverb'

    id = Column(Integer, primary_key=True, autoincrement=True)

    entry_id = Column(Integer, ForeignKey('dictionary_entry.id',
                                          name='FK_dictionary_adverb_entry_id'))

    comparison_type_code = Column(String(10), ForeignKey('type_comparisontype.code',
                                                         name='FK_dictionary_adverb_comparisontype_code'))

    # Relationships
    entry = relationship('Entry', backref=backref('dictionary_adverb'))
    comparison_type = relationship('ComparisonType', backref=backref('dictionary_adverb'))


# Verb Entry
class VerbEntry(Base):
    """Verb entry in the dictionary"""
    __tablename__ = 'dictionary_verb'

    id = Column(Integer, primary_key=True, autoincrement=True)

    entry_id = Column(Integer, ForeignKey('dictionary_entry.id',
                                          name='FK_dictionary_verb_entry_id'))

    conjugation_code = Column(String(10), ForeignKey('type_conjugation.code',
                                                     name='FK_dictionary_verb_conjugation_code'))
    variant = Column(Integer)

    verb_kind_code = Column(String(10), ForeignKey('type_verbkind.code',
                                                   name='FK_dictionary_verb_verbkind_code'))

    # Relationships
    entry = relationship('Entry', backref=backref('dictionary_verb'))
    verb_kind = relationship('VerbKind', backref=backref('dictionary_verb'))


# Preposition Entry
class PrepositionEntry(Base):
    """Preposition entry in the dictionary"""
    __tablename__ = 'dictionary_preposition'

    id = Column(Integer, primary_key=True, autoincrement=True)

    entry_id = Column(Integer, ForeignKey('dictionary_entry.id',
                                          name='FK_dictionary_preposition_entry_id'))

    case_code = Column(String(10), ForeignKey('type_case.code',
                                              name='FK_dictionary_preposition_case_code'))

    # Relationships
    entry = relationship('Entry', backref=backref('dictionary_preposition'))
    case = relationship('Case', backref=backref('dictionary_preposition'))


# Conjunction Entry
class ConjunctionEntry(Base):
    """Conjunction entry in the dictionary"""
    __tablename__ = 'dictionary_conjunction'

    id = Column(Integer, primary_key=True, autoincrement=True)

    entry_id = Column(Integer, ForeignKey('dictionary_entry.id',
                                          name='FK_dictionary_conjunction_entry_id'))

    # Relationships
    entry = relationship('Entry', backref=backref('dictionary_conjunction'))


# Interjection Entry
class InterjectionEntry(Base):
    """Interjection entry in the dictionary"""
    __tablename__ = 'dictionary_interjection'

    id = Column(Integer, primary_key=True, autoincrement=True)

    entry_id = Column(Integer, ForeignKey('dictionary_entry.id',
                                          name='FK_dictionary_interjection_entry_id'))

    # Relationships
    entry = relationship('Entry', backref=backref('dictionary_interjection'))