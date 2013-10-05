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
             u'adj': { u'name': u'adjective',
                     },
             u'conj': { u'name': u'conjunction',
                      },
             u'inj': { u'name': u'injunction',
                     },
             u'dp': { u'name': u'demonstrative particle',
                     },
             u'd': { u'name': u'demonstrative particle',
                     },
             u'np': { u'name': u'negative particle',
                     },
             u'adv': { u'name': u'adverb',
                     },
             u'i': { u'name': u'interrogative particle',
                     },
             u'x': { u'name': u'x',
                     },
             u'n': { u'name': u'noun',
                     u'c': { u'name': u'common', },
                     u'm': { u'name': u'masculine',
                             u'loc':  { u'name': u'locative', },
                          },
                     u'f': { u'name': u'feminine', },
                     u'g': { u'name': u'gentilic', },
                     u'pr': { u'name': u'proper noun',
                            u'm': { u'name': u'masculine', },
                            u'f': { u'name': u'feminine', },
                            u'loc': { u'name': u'locative', },
                           }
                   },
             u'p': { u'name': u'pronoun',
                   },
             u'pron': { u'name': u'pronoun',
                   },
             u'prep': { u'name': u'preposition',
                      },
             u'prt': { u'name': u'particle',
                      },
             u'r': { u'name': u'relative pronoun',
                   },
             u'v': { u'name': u'verb',
                   },
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


if __name__ == '__main__':
  if not os.path.exists(DokuWikiDir):
    os.mkdir(DokuWikiDir)
  dictxml = minidom.parse(StrongFile)
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
