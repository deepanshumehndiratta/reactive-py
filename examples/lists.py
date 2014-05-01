from reactive import _

def foo(trace, *args, **kwargs):
  print 'Trace: ' + str(trace)

# Create a new reactive list
obj = _([1, 2, 3, 4, 5])

obj.onchange(foo, args=(), kwargs={})
 
obj[2] = 4