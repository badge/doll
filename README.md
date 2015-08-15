# Database of Latin Lexicon

The *Database of Latin Lexicon* is an open-source project to create a reliable and complete database of Latin words.

## Latin

Latin is an *inflected* language, which means that the endings of its nouns, verbs, and adjectives change to reflect their meaning. These changes, or inflections, are highly regular, so it makes sense to organise them in some way.

The basic idea behind the DoLL is to separate out the lexical *meaning* of a word from its various inflections. Such lexical meanings are termed *[lexemes](https://en.wikipedia.org/wiki/Lexeme)*.

## DoLL

The DoLL is a continuation of the work of William Whitaker, who created the Latin-English-Latin dictionary [Whitaker’s Words](http://archives.nd.edu/whitaker/words.htm). It comprises three parts. The first is a python program which injests the input files for *Words* (originally written in ADA) and creates the instances of the classes in its object model. The second is a sqlite database created from that object model using [sqlalchemy](http://www.sqlalchemy.org/); the third is a basic word parser (also written in python) for querying the database.