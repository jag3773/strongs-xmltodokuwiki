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


HebrewStrongFile = '../HebrewLexicon/HebrewStrong.xml'
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


if __name__ == '__main__':
  dictxml = minidom.parse(HebrewStrongFile)
  for entryxml in dictxml.getElementsByTagName('entry'):
    token = u''
    xlit = u''
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
    # Get source
    for x in entryxml.getElementsByTagName('source'):
      for i in x.childNodes:
        if i.nodeName == u'note':
          pass
        elif i.nodeName == u'w':
          source.append(u'[[en:strongs:{0}|{1}]]'.format(
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
          meaning.append(u'[[en:strongs:{0}|{1}]]'.format(
                        i.getAttribute('src').lower(), i.getAttribute('src')))
        elif i.nodeName == u'def':
          meaning.append(u'**{0}**'.format(i.firstChild.data))
        else:
          meaning.append(i.data)
    f.write(entryHead.format(entryid, token, xlit, pos, u''.join(source),
                                                          u''.join(meaning)))

    # Get definitions
    for x in entryxml.getElementsByTagName('def'):
      f.write(entryDef.format(x.firstChild.data))

    # Get usage
    for x in entryxml.getElementsByTagName('usage'):
      f.write(entryFooter.format(x.firstChild.data))

    f.close()
