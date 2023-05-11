#!/usr/bin/env python3
import sys
import re

START = '<span class="c1">// BTEST</span>'
END='<span class="c1">// ETEST</span>'
html_path = sys.argv[1].rstrip()
with open(html_path, 'r') as content_file:
    content = content_file.read()

def replaceTextBetween(originalText, delimeterA, delimterB, replacementText):
    index_from = 0
    index_to = len(originalText)
    if delimeterA in originalText:
        index_from = originalText.index(delimeterA)

    if delimterB in originalText:
        index_to = originalText.index(delimterB) + len(delimterB)

    return originalText[0:index_from] + originalText[index_to:]

while START in content:
    content = replaceTextBetween(content, START, END, '')
with open(html_path, 'w+') as stream:
    stream.write(content)
