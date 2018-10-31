
from lxml import html, etree

doc = html.fromstring(open('a.html').read())
out = open('a.xhtml', 'wb')
out.write(etree.tostring(doc))
