# Database of Latin Lexicon

The *Database of Latin Lexicon* is an open-source project to create a reliable and complete database of Latin words.

## Latin

Latin is an *inflected* language, which means that the endings of its nouns, verbs, and adjectives change to reflect their meaning. These changes, or inflections, are highly regular, so it makes sense to organise them in some way.

The basic idea behind the DoLL is to separate out the lexical *meaning* of a word from its various inflections. Such lexical meanings are termed *[lexemes](https://en.wikipedia.org/wiki/Lexeme)*.

## DoLL

The DoLL is a continuation of the work of William Whitaker, who created the Latin-English-Latin dictionary [Whitaker’s Words](http://archives.nd.edu/whitaker/words.htm). It comprises three parts. The first is a python program which ingests the input files for *Words* (originally written in ADA) and creates the instances of the classes in its object model. The second is a sqlite database created from that object model using [sqlalchemy](http://www.sqlalchemy.org/); the third is a basic word parser (also written in python) for querying the database.

## Current status

Firstly, two things should be noted about the software:

1. Nothing is in its final form.
2. Changes between versions **will not** preserve backward compatibility.

At this point, the DoLL has no version number, to highlight the fact that it is currently an exploration rather than being on a path to success. *Words* is hugely impressive, but its architecture is limited by the structure of its inputs, and creating a normalised database from those inputs is less than straightforward. The following things are currently identified as significant challenges:

- **parse_test.py currently handles only nouns, verbs, and pronouns**
  - This is just a case of creating the queries for the other part of speech codes, but as these are created other problems arise than need considering.
- **There is no English-Latin translation**
  - In *Words*, this is much more structurally straightforward as this is a word search on the dictionary, and for English lexemes that do inflect (verbs and pronouns) there is no attempt to link the various inflections between the two languages. Given how irregular English is, that seems completely sensible, but it does mean that the amount of effort to create the English-Latin part of a parser would be very slight.
- **Neither dictionary entries nor inflections have macrons**
  - I am currently in two minds as to whether to alter the input files, or to create some way of updating them once they have been ingested by the application but before being added to the database. I would like to see *Words* as complete, but realistically I think it unlikely that the DoLL check 39k different words and 2,000 inflections on first creation. While the database schema is still in flux it would seem silly to move to it as the single source of truth before time. It would likely be possible to implement general rules such as those described [here](http://rharriso.sites.truman.edu/latin_vowel-quantity_macrons_macra/), but that would not be a solution in the long-term/
- **Translations are not handled well**
  - Translations are currently stored in a single column in the dictionary_entry table (the Entry class). This needs sorting soon, as Whitaker left clear definitions on the structure of translations (,;: all have different meanings). It also limits the use of the DoLL to English, which, while popular, is not universal.
- **Addons are ignored**
  - Prefixes, suffixes, and the like, are handled in *Words* by the addons_package and generated from the ADDONS.LAT file. These are not used at all by the DoLL, but are definitely something we want to add support for.
- **qu/cu pronouns are a mess**
  - These pronouns have multiple dictionary and inflection entries, created for computational convenience, but this leads to duplicate results when parsing words