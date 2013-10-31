#!/usr/bin/env python
# -*- coding: utf8 -*-
#  Copyright (c) 2012-2013 Jesse Griffin
#  Some code from https://github.com/jag3773/d-bdb
#  http://creativecommons.org/licenses/MIT/
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

import os
import codecs
from xml.dom import minidom


StrongFile = '../HebrewLexicon/HebrewStrong.xml'
DokuWikiDir = 'DokuWikiStrongsHebrew'
reflink = u'  * [[en:lexicon:{0}|{1}]]\n'
navlink = u'[[en:lexicon:hebrew-{0}|{1}]]'
xlitHeader = u'''**Navigation**
{0}
----

===== {1} =====

'''
IndexHeader = u'''**Navigation**
[[en:lexicon:hebrew-numbers-1|1-1000]] - 
[[en:lexicon:hebrew-numbers-1001|1001-2000]] - 
[[en:lexicon:hebrew-numbers-2001|2001-3000]] - 
[[en:lexicon:hebrew-numbers-3001|3001-4000]] - 
[[en:lexicon:hebrew-numbers-4001|4001-5000]] - 
[[en:lexicon:hebrew-numbers-5001|5001-6000]] -
[[en:lexicon:hebrew-numbers-6001|6001-7000]] -
[[en:lexicon:hebrew-numbers-7001|7001-8000]] -
[[en:lexicon:hebrew-numbers-8001|8001-8674]]
----

===== Strongs Hebrew Index: {0} - {1} =====

'''
entryHead = u'''====== {0}: {1} ({2}) ======

===== Part of Speech =====

{3}

===== Source =====

{4}

===== Meaning =====

{5}

===== Definitions =====

'''
entryDef = u'  - {0}\n'
entryFooter = u'''
===== Usage =====

{0}
'''
# Part of speech translation table
postrans = { u'a': { u'name': u'adjective',
                    u'm': { u'name': u'masculine', },
                    u'f': { u'name': u'feminine', },
                    u'a': { u'name': u'adjective', },
                    u'c': { u'name': u'cardinal number', },
                    u'g': { u'name': u'gentilic', },
                    u'gent': { u'name': u'gentilic', },
                    u'o': { u'name': u'ordinal number', },
                   },
             u'adv': { u'name': u'adverb',
                     },
             u'conj': { u'name': u'conjunction',
                      },
             u'd': { u'name': u'demonstrative pronoun',
                     },
             u'da': { u'name': u'definite article',
                     },
             u'dp': { u'name': u'demonstrative particle',
                     },
             u'i': { u'name': u'interrogative pronoun',
                     },
             u'inj': { u'name': u'interjection',
                     },
             u'x': { u'name': u'indefinite pronoun',
                     },
             u'n': { u'name': u'noun',
                     u'c': { u'name': u'common', },
                     u'm': { u'name': u'masculine',
                             u'loc':  { u'name': u'location', },
                          },
                     u'f': { u'name': u'feminine', },
                     u'g': { u'name': u'gentilic', },
                     u'pr': { u'name': u'proper noun',
                            u'm': { u'name': u'masculine', },
                            u'f': { u'name': u'feminine', },
                            u'loc': { u'name': u'location', },
                           }
                   },
             u'np': { u'name': u'negative particle',
                     },
             u'p': { u'name': u'personal pronoun',
                   },
             u'prep': { u'name': u'preposition',
                      },
             u'pron': { u'name': u'pronoun',
                   },
             u'prt': { u'name': u'particle',
                      },
             u'r': { u'name': u'relative pronoun',
                   },
             u'rpt': { u'name': u'relative particle',
                   },
             u'v': { u'name': u'verb',
                   },
}
xlittable = { u'\u02bb': u'A',
              u'B': u'B',
              u'D': u'D',
              u'\xc7': u'C',
              u'H': u'H',
              u'L': u'L',
              u'N': u'N',
              u'P': u'P',
              u'R': u'R',
              u'T': u'T',
              u'V': u'V',
              u'Z': u'Z',
              u'\u05e1': u'S',
              u'b': u'B',
              u'd': u'D',
              u'\xe7': u'C',
              u'\u05e9': u'S',
              u'h': u'H',
              u'\u1e6c': u'T',
              u'n': u'N',
              u'p': u'P',
              u'r': u'R',
              u't': u'T',
              u'v': u'V',
              u'z': u'Z',
              u'\u1e6d': u'T',
              u'l': u'L',
              u'\u02bc': u'A',
              u'C': u'C',
              u'G': u'G',
              u'K': u'K',
              u'M': u'M',
              u'Q': u'Q',
              u'S': u'S',
              u'Y': u'Y',
              u'\u05d8': u'T',
              u'\u05dc': u'L',
              u'c': u'C',
              u'g': u'G',
              u'\u05e6': u'T',
              u'k': u'K',
              u'm': u'M',
              u'q': u'Q',
              u's': u'S',
              u'y': u'Y'
}


def getParsing(pos):
  parsing = []
  parts = pos.split('-')
  for i in parts:
    if len(parsing) == 0:
      parsing.append(postrans[parts[0]]['name'])
    elif len(parsing) == 1:
      if len(parts) == 2:
        parsing.append(postrans[parts[0]][i]['name'])
      elif len(parts) == 3:
        parsing.append(postrans[parts[0]][i]['name'])
    elif len(parsing) == 2:
      parsing.append(postrans[parts[0]][parts[1]][i]['name'])
  return u' - '.join(parsing)

def splitlist(l, n):
  '''
  A generator that returns items in a list chunked by n.
  '''
  for i in xrange(0, len(l), n):
    yield (i+1, n, l[i:i+n])


if __name__ == '__main__':
  if not os.path.exists(DokuWikiDir):
    os.mkdir(DokuWikiDir)
  dictxml = minidom.parse(StrongFile)
  xlitheaders = []
  indexlist = []
  xlitindexlist = []
  for entryxml in dictxml.getElementsByTagName('entry'):
    token = u''
    xlit = u''
    parsing = u''
    source = []
    meaning = []
    entryid = entryxml.getAttribute('id')
    filename = '{0}.txt'.format(entryid.lower())
    f = codecs.open('{0}/{1}'.format(DokuWikiDir, filename), 'w',
                                                             encoding='utf-8')
    # Get word
    for x in entryxml.getElementsByTagName('w'):
      if x.hasAttribute('xml:lang'):
        token = x.firstChild.data
        xlit = x.getAttribute('xlit')
        pos = x.getAttribute('pos')
        for item in pos.split(' '):
          parsing += getParsing(item)
    # Get source
    for x in entryxml.getElementsByTagName('source'):
      for i in x.childNodes:
        if i.nodeName == u'note':
          pass
        elif i.nodeName == u'w':
          source.append(u'[[en:lexicon:{0}|{1}]]'.format(
                        i.getAttribute('src').lower(), i.getAttribute('src')))
        elif i.nodeName == u'def':
          source.append(u'**{0}**'.format(i.firstChild.data))
        else:
          source.append(i.data)
    # Get meaning
    for x in entryxml.getElementsByTagName('meaning'):
      for i in x.childNodes:
        if i.nodeName == u'note':
          pass
        elif i.nodeName == u'w':
          meaning.append(u'[[en:lexicon:{0}|{1}]]'.format(
                        i.getAttribute('src').lower(), i.getAttribute('src')))
        elif i.nodeName == u'def':
          meaning.append(u'**{0}**'.format(i.firstChild.data))
        else:
          meaning.append(i.data)
    f.write(entryHead.format(entryid, token, xlit, parsing, u''.join(source),
                                                          u''.join(meaning)))

    # Get definitions
    for x in entryxml.getElementsByTagName('def'):
      f.write(entryDef.format(x.firstChild.data))

    # Get usage
    for x in entryxml.getElementsByTagName('usage'):
      f.write(entryFooter.format(x.firstChild.data))

    f.close()
    indexlist.append(reflink.format(entryid.lower(), entryid))
    xlitindexlist.append((xlit, reflink.format(entryid.lower(), xlit)))

  # Write xlit index files
  xlitheaders = set(sorted([xlittable[x[0][0]] for x in xlitindexlist
                                                             if x[0] != u'']))
  xlitnavigation = u' - '.join([navlink.format(x.lower(), x) for x in
                                                                 xlitheaders])
  for x in xlitheaders:
    xlitIndexFile = u'{0}/hebrew-{1}.txt'.format(DokuWikiDir, x.lower())
    xlitindex = codecs.open(xlitIndexFile, 'w', encoding='utf-8')
    xlitindex.write(xlitHeader.format(xlitnavigation, x))
    xlitindex.close()
  for x in xlitindexlist:
    if x[0] == u'': continue
    xlitIndexFile = u'{0}/hebrew-{1}.txt'.format(DokuWikiDir,
                                                   xlittable[x[0][0]].lower())
    xlitindex = codecs.open(xlitIndexFile, 'a', encoding='utf-8')
    xlitindex.write(x[1])
    xlitindex.close()

  # Write numerical index files
  for x in splitlist(indexlist, 1000):
    IndexFile = '{0}/hebrew-numbers-{1}.txt'.format(DokuWikiDir, x[0])
    index = codecs.open(IndexFile, 'w', encoding='utf-8')
    index.write(IndexHeader.format(x[0], (x[0] + len(x[2]) - 1)))
    for i in x[2]:
      index.write(i)
    index.close()
