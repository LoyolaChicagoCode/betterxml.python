#
# This is just a brief demo of how a Python-like schema will look.
#
# The dream is that this model can be used to generate a DTD, W3 Schema, or RELAX-NG.
# We'll also be able to generate interfaces for data binding (to Better XML, of course)



from betterxml.schema import *

dtd = Schema("http://www.tempuri.org")

ticket = dtd.Element('ticket')
seq = dtd.Element('seq')
job = dtd.Element('job')
par = dtd.Element('par')
property = dtd.Element('property')
ticket.model = (job | seq | par)

print dtd.elements
print

ticket.pprint(0)

print

ticket.model.pprint(0)

ticket.model = closure(job | seq | par)

ticket.model.pprint(0)