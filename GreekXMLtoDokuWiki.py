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


StrongFile = '../strongs-dictionary-xml/strongsgreek.xml'
DokuWikiDir = 'DokuWikiStrongsGreek'
reflink = u'  * [[en:lexicon:{0}|{1}]]\n'
IndexHeader = u'''**Navigation**
[[en:lexicon:greek-numbers-1|1-1000]] - 
[[en:lexicon:greek-numbers-1001|1001-2000]] - 
[[en:lexicon:greek-numbers-2001|2001-3000]] - 
[[en:lexicon:greek-numbers-3001|3001-4000]] - 
[[en:lexicon:greek-numbers-4001|4001-5000]] - 
[[en:lexicon:greek-numbers-5001|5001-5624]]
----

===== Strongs Greek Index: {0} - {1} =====

'''
navlink = u'[[en:lexicon:greek-{0}|{1}]]'
xlitHeader = u'''**Navigation**
{0}
----

===== {1} =====

'''
entryHead = u'''====== {0}: {1} ({2}) ======

===== Source =====

{3}

===== Meaning =====

{4}

===== Usage =====

{5}

===== Strongs References =====

{6}
'''
xlittable = { u'Á': 'A',
              u'ō': 'O',
              u'í': 'I',
              u'ē': 'E',
              u'Ē': 'E',
              u'ḗ': 'E',
              u'Ḗ': 'E',
              u'î': 'I',
              u'é': 'E',
              u'Ō': 'O',
              u'ó': 'O',
              u'É': 'E',
              u'ṓ': 'O',
              u'â': 'A',
              u'A': 'A',
              u'á': 'A',
              u'C': 'C',
              u'B': 'B',
              u'E': 'E',
              u'D': 'D',
              u'G': 'G',
              u'I': 'I',
              u'H': 'H',
              u'K': 'K',
              u'M': 'M',
              u'L': 'L',
              u'O': 'O',
              u'N': 'N',
              u'P': 'P',
              u'S': 'S',
              u'R': 'R',
              u'T': 'T',
              u'Z': 'Z',
              u'a': 'A',
              u'c': 'C',
              u'b': 'B',
              u'e': 'E',
              u'd': 'D',
              u'g': 'G',
              u'i': 'I',
              u'h': 'H',
              u'k': 'K',
              u'm': 'M',
              u'l': 'L',
              u'o': 'O',
              u'n': 'N',
              u'p': 'P',
              u's': 'S',
              u'r': 'R',
              u't': 'T',
              u'x': 'X',
              u'z': 'Z',
              u'-': 'P'
              }

def getStrongsref(i):
  '''
  Returns a unicode string with the Strongs reference number, including the
  language code, in DokuWiki link format.
  '''
  ref = u'{0}{1}'.format(i.getAttribute(u'language')[0],
                                     i.getAttribute(u'strongs'))
  return u'[[en:lexicon:{0}|{1}]]'.format(ref.lower(), ref)

def getGreek(i):
  '''
  Returns a tuple of the unicode and transliteration values.
  '''
  return (i.getAttribute(u'unicode'), i.getAttribute(u'translit'))

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
  indexlist = []
  xlitindexlist = []
  for entryxml in dictxml.getElementsByTagName('entry'):
    token = u''
    xlit = u''
    parsing = u''
    source = []
    meaning = []
    strongsrefs = []
    usage = u''
    entryid = u'G{0}'.format(entryxml.getAttribute(u'strongs').lstrip('0'))
    filename = '{0}.txt'.format(entryid.lower())
    # Get word
    try:
      token, xlit = getGreek(entryxml.getElementsByTagName(u'greek')[0])
    except:
      f = codecs.open('{0}/{1}'.format(DokuWikiDir, filename), 'w',
                                                             encoding='utf-8')
      f.write(entryHead.format(entryid, u'Not Used', u'', u'', u'', u'', u''))
      f.close()
    # Get source
    for x in entryxml.getElementsByTagName(u'strongs_derivation'):
      for i in x.childNodes:
        if i.nodeName == u'strongsref':
          source.append(getStrongsref(i))
        elif i.nodeName == u'greek':
          g1, g2 = getGreek(i)
          source.append(u'{0} ({1})'.format(g1, g2))
        elif i.nodeName == u'latin':
          source.append(i.firstChild.data)
        elif i.nodeName == u'pronunciation':
          pass
        else:
          source.append(i.data)
    # Get meaning
    for x in entryxml.getElementsByTagName(u'strongs_def'):
      meaning.append(x.firstChild.data.replace('\n', '').strip())
    # Get usage
    for x in entryxml.getElementsByTagName(u'kjv_def'):
      usage = x.firstChild.data.replace('\n', '').strip().replace(':--', '')

    # Get strongs references
    for x in entryxml.getElementsByTagName(u'see'):
      strongsrefs.append(u'  - {0}'.format(getStrongsref(x)))
    # Write file
    f = codecs.open('{0}/{1}'.format(DokuWikiDir, filename), 'w',
                                                             encoding='utf-8')
    f.write(entryHead.format(entryid, token, xlit, u''.join(source),
                           u''.join(meaning), usage, u'\n'.join(strongsrefs)))
    f.close()
    indexlist.append(reflink.format(entryid.lower(), entryid))
    xlitindexlist.append((xlit, reflink.format(entryid.lower(), xlit)))

  # Write xlit index files
  xlitheaders = set(sorted([xlittable[x[0][0]] for x in xlitindexlist
                                                             if x[0] != u'']))
  xlitnavigation = u' - '.join([navlink.format(x.lower(), x) for x in
                                                                 xlitheaders])
  for x in xlitheaders:
    xlitIndexFile = u'{0}/greek-{1}.txt'.format(DokuWikiDir, x.lower())
    xlitindex = codecs.open(xlitIndexFile, 'w', encoding='utf-8')
    xlitindex.write(xlitHeader.format(xlitnavigation, x))
    xlitindex.close()
  for x in xlitindexlist:
    if x[0] == u'': continue
    xlitIndexFile = u'{0}/greek-{1}.txt'.format(DokuWikiDir,
                                                   xlittable[x[0][0]].lower())
    xlitindex = codecs.open(xlitIndexFile, 'a', encoding='utf-8')
    xlitindex.write(x[1])
    xlitindex.close()

  # Write numerical index files
  for x in splitlist(indexlist, 1000):
    IndexFile = u'{0}/greek-numbers-{1}.txt'.format(DokuWikiDir, x[0])
    index = codecs.open(IndexFile, 'w', encoding='utf-8')
    index.write(IndexHeader.format(x[0], (x[0] + len(x[2]) - 1)))
    for i in x[2]:
      index.write(i)
    index.close()
