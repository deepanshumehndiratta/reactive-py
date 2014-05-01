from reactive import _

def foo(trace, *args, **kwargs):
  print 'Trace: ' + str(trace)

# Create a new reactive <'type' int> object
obj = _(1)

obj.onchange(foo, args=(), kwargs={})

# Assign value 2 to the object while keeping all its hooks (onchange, oncompare, before_call, after_call, etc) if any, intact and trigger a onchange event simultaneously
 
obj._(2)