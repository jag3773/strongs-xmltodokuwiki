strongs-xmltodokuwiki
==========

Converts Strongs XML files to DokuWiki formatted files which are named after
their Strongs number.  This is simply a document conversion script.  No changes
are made to the data, although some data is not included in the DokuWiki files,
for example, the pronounciation is not included.

The Hebrew Strongs conversion script requires HebrewStrong.xml from
https://github.com/openscriptures/HebrewLexicon.  By default, it assumes that
this repo is one level up, it loads "../HebrewLexicon/HebrewStrong.xml".

The Greek Strongs conversion script requires strongsgreek.xml from
https://github.com/morphgnt/strongs-dictionary-xml.  By default, it assumes
that this repo is one level up, it loads
"../strongs-dictionary-xml/strongsgreek.xml".


TODO
==========

Strongs Hebrew
----------

* Inline BDB

* Add TWOT references

Strongs Greek
----------

