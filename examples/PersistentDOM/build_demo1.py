#
# If this goes well, a directory would be created containing the persistent
# representation of a document
#

from xml.sax import saxexts

from pparser import PElementParser
from os import system
system('rm -rf xyz')
pp = PElementParser('xyz', saxexts.make_parser())
pp.process('test1.xml')
