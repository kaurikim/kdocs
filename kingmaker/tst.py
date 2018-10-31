
import BeautifulSoup
f = open('a.html')
soup = BeautifulSoup.BeautifulSoup(f)
f.close()


print soup.title
# <title>The Dormouse's story</title>

print soup.title.name
# u'title'

print soup.title.string
# u'The Dormouse's story'

print '.....'
print soup
print '.....'
print soup.title.parent.name
# u'head'

print soup.p
# <p class="title"><b>The Dormouse's story</b></p>

soup.p['div']
# u'title'

print soup.a
# <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>

# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

print soup.find(id="link3")
# <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>

#g = open('a.xml', 'w')
#print >> g, soup.prettify()
#g.close()
