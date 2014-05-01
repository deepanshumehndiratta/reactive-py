from reactive import _

def foo(trace, *args, **kwargs):
  print 'Trace: ' + str(trace)

# Create a new reactive tuple
obj = _(('a', 'b'))

obj.onchange(foo, args=(), kwargs={})
 
obj += ('c', 'd')