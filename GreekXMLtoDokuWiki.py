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
IndexFile = '{0}/greek-numbers.txt'.format(DokuWikiDir)
reflink = u'  - [[en:lexicon:{0}|{1}]]\n'
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


if __name__ == '__main__':
  if not os.path.exists(DokuWikiDir):
    os.mkdir(DokuWikiDir)
  dictxml = minidom.parse(StrongFile)
  index = codecs.open(IndexFile, 'w', encoding='utf-8')
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
    index.write(reflink.format(entryid.lower(), entryid))
  index.close()
