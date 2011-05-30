
# Note: using properties *requires* that the class is a bona-fide 'object'.
# The new python classes must explicitly (through some path of inheritance)
# have object as a base class.

class prop1(object):
   def __init__(self):
      self.__state = { 'x' : 25, 'y' : 30 }

   def get_x(self): return self.__state['x']

   def set_x(self, new_x): self.__state['x'] = new_x

   def get_y(self): return self.__state['y']

   # allow r/w access to 'x'
   x = property(get_x, set_x, doc="X r/w property")
   y = property(get_y, None, doc="Y ro property")

   def __str__(self): return str(self.__state)

p = prop1()
print 'p=',p
print 'p.x=',p.x
print 'p.y=',p.y
print 'p docs=',p.__doc__

try:
  print "setting p.x"
  p.x = 50
  print "setting p.y"
  p.y = 100
except:
  print "This exception should occur for p.y!"

print "after try"
print 'p=',p
print 'p.x=',p.x
print 'p.y=',p.y
print 'p docs=',p.__doc__
