from reactive import _

def foo(trace, *args, **kwargs):
  print 'Trace: ' + str(trace)

# Create a new reactive dict
obj = _({'a': 'b', 'c': 'd'})

obj.onchange(foo, args=(), kwargs={})
 
obj['e'] = 'f'