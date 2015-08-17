""" Creates the basic database types and populates the database.
    
    
"""

__author__ = 'Matthew Badger'

from doll_db.model import *


# Add the basic database types
def create_type_contents():
    Connection.session.add(Number(code='X', name='Unknown', description=''))
    Connection.session.add(Number(code='S', name='Singular', description=''))
    Connection.session.add(Number(code='P', name='Plural', description=''))

    Connection.session.add(
        WordAge(code='X', name='Universal', description='In use throughout the ages/unknown -- the default'))
    Connection.session.add(
        WordAge(code='A', name='Archaic', description='Very early forms, obsolete by classical times'))
    Connection.session.add(
        WordAge(code='B', name='Early', description='Early Latin, pre-classical, used for effect/poetry'))
    Connection.session.add(WordAge(code='C', name='Classical', description='Limited to classical (~150 BC - 200 AD)'))
    Connection.session.add(WordAge(code='D', name='Late', description='Late, post-classical (3rd-5th centuries)'))
    Connection.session.add(
        WordAge(code='E', name='Later', description='Latin not in use in Classical times (6-10), Christian'))
    Connection.session.add(WordAge(code='F', name='Medieval', description='Medieval (11th-15th centuries)'))
    Connection.session.add(
        WordAge(code='G', name='Scholar', description='Latin post 15th - Scholarly/Scientific   (16-18)'))
    Connection.session.add(
        WordAge(code='H', name='Modern', description='Coined recently, words for new things (19-20)'))

    Connection.session.add(WordFrequency(code='X', name='Universal', description='Unknown or unspecified'))
    Connection.session.add(
        WordFrequency(code='A', name='Very frequent', description='Very frequent, in all Elementary Latin books'))
    Connection.session.add(WordFrequency(code='B', name='Frequent', description='Frequent, in top 10 percent'))
    Connection.session.add(WordFrequency(code='C', name='Common', description='For Dictionary, in top 10,000 words'))
    Connection.session.add(WordFrequency(code='D', name='Lesser', description='For Dictionary, in top 20,000 words'))
    Connection.session.add(WordFrequency(code='E', name='Uncommon', description='2 or 3 citations'))
    Connection.session.add(
        WordFrequency(code='F', name='Very rare', description='Having only single citation in OLD or L+S'))
    Connection.session.add(WordFrequency(code='I', name='Inscription', description='Only citation is inscription'))
    Connection.session.add(WordFrequency(code='M', name='Graffiti', description='Presently not much used'))
    Connection.session.add(
        WordFrequency(code='N', name='Pliny', description='Things that appear (almost) only in Pliny Natural History'))

    Connection.session.add(WordArea(code='X', name='All', description='All or none'))
    Connection.session.add(
        WordArea(code='A', name='Agriculture', description='Agriculture, Flora, Fauna, Land, Equipment, Rural'))
    Connection.session.add(WordArea(code='B', name='Biological', description='Biological, Medical, Body Parts'))
    Connection.session.add(
        WordArea(code='D', name='Drama', description='Drama, Music, Theater, Art, Painting, Sculpture'))
    Connection.session.add(WordArea(code='E', name='Ecclesiastic', description='Ecclesiastic, Biblical, Religious'))
    Connection.session.add(
        WordArea(code='G', name='Grammar', description='Grammar, Retoric, Logic, Literature, Schools'))
    Connection.session.add(
        WordArea(code='L', name='Legal', description='Legal, Government, Tax, Financial, Political, Titles'))
    Connection.session.add(WordArea(code='P', name='Poetic', description='Poetic'))
    Connection.session.add(
        WordArea(code='S', name='Science', description='Science, Philosophy, Mathematics, Units/Measures'))
    Connection.session.add(
        WordArea(code='T', name='Technical', description='Technical, Architecture, Topography, Surveying'))
    Connection.session.add(WordArea(code='W', name='War', description='War, Military, Naval, Ships, Armor'))
    Connection.session.add(WordArea(code='Y', name='Mythology', description='Mythology'))

    Connection.session.add(WordLocation(code='X', name='All', description='All or none'))
    Connection.session.add(WordLocation(code='A', name='Africa', description='Africa'))
    Connection.session.add(WordLocation(code='B', name='Britain', description='Britain'))
    Connection.session.add(WordLocation(code='C', name='China', description='China'))
    Connection.session.add(WordLocation(code='D', name='Scandinavia', description='Scandinavia'))
    Connection.session.add(WordLocation(code='E', name='Egypt', description='Egypt'))
    Connection.session.add(WordLocation(code='F', name='France', description='France, Gaul'))
    Connection.session.add(WordLocation(code='G', name='Germany', description='Germany'))
    Connection.session.add(WordLocation(code='H', name='Greece', description='Greece'))
    Connection.session.add(WordLocation(code='I', name='Italy', description='Italy, Rome'))
    Connection.session.add(WordLocation(code='J', name='India', description='India'))
    Connection.session.add(WordLocation(code='K', name='Balkans', description='Balkans'))
    Connection.session.add(WordLocation(code='N', name='Netherlands', description='Netherlands'))
    Connection.session.add(WordLocation(code='P', name='Persia', description='Persia'))
    Connection.session.add(WordLocation(code='Q', name='Near', description='Near East'))
    Connection.session.add(WordLocation(code='R', name='Russia', description='Russia'))
    Connection.session.add(WordLocation(code='S', name='Spain', description='Spain, Iberia'))
    Connection.session.add(WordLocation(code='U', name='Eastern', description='Eastern Europe'))

    Connection.session.add(WordSource(code='X', name='', description='General or unknown or too common to say'))
    Connection.session.add(WordSource(code='A', name='', description='Unused'))
    Connection.session.add(
        WordSource(code='B', name='Bee', description='C.H.Beeson, A Primer of Medieval Latin, 1925 (Bee)'))
    Connection.session.add(
        WordSource(code='C', name='Cas', description='Charles Beard, Cassell\'s Latin Dictionary 1892 (Cas)'))
    Connection.session.add(
        WordSource(code='D', name='Sex', description='J.N.Adams, Latin Sexual Vocabulary, 1982 (Sex)'))
    Connection.session.add(
        WordSource(code='E', name='Ecc', description='L.F.Stelten, Dictionary of Eccles. Latin, 1995 (Ecc)'))
    Connection.session.add(
        WordSource(code='F', name='DeF', description='Roy J. Deferrari, Dictionary of St. Thomas Aquinas, 1960 (DeF)'))
    Connection.session.add(
        WordSource(code='G', name='G+L', description='Gildersleeve + Lodge, Latin Grammar 1895 (G+L)'))
    Connection.session.add(WordSource(code='H', name='', description='Collatinus Dictionary by Yves Ouvrard'))
    Connection.session.add(
        WordSource(code='I', name='', description='Leverett, F.P., Lexicon of the Latin Language, Boston 1845'))
    Connection.session.add(WordSource(code='J', name='', description='Bracton: De Legibus Et Consuetudinibus Angli�'))
    Connection.session.add(
        WordSource(code='K', name='Cal', description='Calepinus Novus, modern Latin, by Guy Licoppe (Cal)'))
    Connection.session.add(WordSource(code='L', name='', description='Lewis, C.S., Elementary Latin Dictionary 1891'))
    Connection.session.add(
        WordSource(code='M', name='Latham', description='Latham, Revised Medieval Word List, 1980 (Latham)'))
    Connection.session.add(WordSource(code='N', name='Nel', description='Lynn Nelson, Wordlist (Nel)'))
    Connection.session.add(WordSource(code='O', name='OLD', description='Oxford Latin Dictionary, 1982 (OLD)'))
    Connection.session.add(WordSource(code='P', name='Souter',
                                      description='Souter, A Glossary of Later Latin to 600 A.D., Oxford 1949 (Souter)'))
    Connection.session.add(WordSource(code='Q', name='', description='Other, cited or unspecified dictionaries'))
    Connection.session.add(WordSource(code='R', name='Plater',
                                      description='Plater + White, A Grammar of the Vulgate, Oxford 1926 (Plater)'))
    Connection.session.add(
        WordSource(code='S', name='L+S', description='Lewis and Short, A Latin Dictionary, 1879 (L+S)'))
    Connection.session.add(
        WordSource(code='T', name='', description='Found in a translation  --  no dictionary reference'))
    Connection.session.add(WordSource(code='U', name='', description=''))
    Connection.session.add(
        WordSource(code='V', name='Saxo', description='Vademecum in opus Saxonis - Franz Blatt (Saxo)'))
    Connection.session.add(WordSource(code='W', name='Whitaker',
                                      description='My personal guess, mostly obvious extrapolation (Whitaker or W)'))
    Connection.session.add(WordSource(code='Y', name='', description='Temp special code'))
    Connection.session.add(WordSource(code='Z', name='', description='Sent by user --  no dictionary reference'))

    Connection.session.add(Gender(code='X', name='Unknown', description='All, none, or unknown'))
    Connection.session.add(Gender(code='M', name='Masculine', description=''))
    Connection.session.add(Gender(code='F', name='Feminine', description=''))
    Connection.session.add(Gender(code='N', name='Neuter', description=''))
    Connection.session.add(Gender(code='C', name='Common', description='Masculine and/or Feminine'))

    Connection.session.add(
        Case(code='X', name='All, none, or unknown', description='', is_default=True, uk_order=0, us_order=0))
    Connection.session.add(Case(code='NOM', name='Nominative', description='', is_default=True, uk_order=1, us_order=1))
    Connection.session.add(Case(code='VOC', name='Vocative', description='', is_default=False, uk_order=2, us_order=2))
    Connection.session.add(Case(code='ACC', name='Accusative', description='', is_default=True, uk_order=3, us_order=6))
    Connection.session.add(Case(code='GEN', name='Genitive', description='', is_default=True, uk_order=4, us_order=3))
    Connection.session.add(Case(code='DAT', name='Dative', description='', is_default=True, uk_order=5, us_order=4))
    Connection.session.add(Case(code='ABL', name='Ablative', description='', is_default=True, uk_order=6, us_order=5))
    Connection.session.add(Case(code='LOC', name='Locative', description='', is_default=True, uk_order=7, us_order=7))

    Connection.session.add(Declension(code=0, name='Unknown', description='', order=0))
    Connection.session.add(Declension(code=1, name='First', description='', order=1))
    Connection.session.add(Declension(code=2, name='Second', description='', order=2))
    Connection.session.add(Declension(code=3, name='Third', description='', order=3))
    Connection.session.add(Declension(code=4, name='Fourth', description='', order=4))
    Connection.session.add(Declension(code=5, name='Fifth', description='', order=5))
    Connection.session.add(Declension(code=6, name='Sixth', description='', order=6))
    Connection.session.add(Declension(code=7, name='Sixth', description='', order=7))
    Connection.session.add(Declension(code=8, name='Sixth', description='', order=8))
    Connection.session.add(Declension(code=9, name='Sixth', description='', order=9))

    Connection.session.add(NounKind(code='X', name='', description='unknown, nondescript'))
    Connection.session.add(NounKind(code='S', name='', description='Singular "only"'))
    Connection.session.add(NounKind(code='M', name='', description='plural or Multiple "only"'))
    Connection.session.add(NounKind(code='A', name='', description='Abstract idea'))
    Connection.session.add(NounKind(code='G', name='', description='Group/collective Name -- Roman(s)'))
    Connection.session.add(NounKind(code='N', name='', description='proper Name'))
    Connection.session.add(NounKind(code='P', name='', description='a Person'))
    Connection.session.add(NounKind(code='T', name='', description='a Thing'))
    Connection.session.add(NounKind(code='L', name='', description='Locale, name of country/city'))
    Connection.session.add(NounKind(code='W', name='', description='a place Where'))

    Connection.session.add(Person(code=0, name='Unknown', description='All, none, or unknown'))
    Connection.session.add(Person(code=1, name='First', description=''))
    Connection.session.add(Person(code=2, name='Second', description=''))
    Connection.session.add(Person(code=3, name='Third', description=''))

    Connection.session.add(Tense(code='X', name='Unknown', description='All, none, or unknown'))
    Connection.session.add(Tense(code='PRES', name='Present', description=''))
    Connection.session.add(Tense(code='IMPF', name='Imperfect', description=''))
    Connection.session.add(Tense(code='FUT', name='Future', description=''))
    Connection.session.add(Tense(code='PERF', name='Perfect', description=''))
    Connection.session.add(Tense(code='PLUP', name='Pluperfect', description=''))
    Connection.session.add(Tense(code='FUTP', name='Future Perfect', description=''))

    Connection.session.add(Voice(code='X', name='Unknown', description='All, none, or unknown'))
    Connection.session.add(Voice(code='ACTIVE', name='Active', description=''))
    Connection.session.add(Voice(code='PASSIVE', name='Passive', description=''))

    Connection.session.add(Mood(code='X', name='Unknown', description='All, none, or unknown'))
    Connection.session.add(Mood(code='IND', name='Indicative', description=''))
    Connection.session.add(Mood(code='SUB', name='Subjunctive', description=''))
    Connection.session.add(Mood(code='IMP', name='Imperative', description=''))
    Connection.session.add(Mood(code='INF', name='Infinitive', description=''))
    Connection.session.add(Mood(code='PPL', name='Participle', description=''))

    Connection.session.commit()
