from reactive import _

def foo(trace, *args, **kwargs):
  print 'Trace: ' + str(trace)

class A:
  pass

# Create a new reactive <'type' int> object
obj = _(A())

obj.onchange(foo, args=(), kwargs={})
 
obj.a = 'B'
obj.a = 'C'