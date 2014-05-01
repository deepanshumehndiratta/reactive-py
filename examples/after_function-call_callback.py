from reactive import _

def foo(bar=None, baz=None):
  print 'bar: ' + str(bar)
  print 'baz: ' + str(baz)
  return "Return Value"

def printer(trace, *args, **kwargs):
  print 'Trace: ' + str(trace)
 
foo_obj = _(foo)

foo_obj.after_call(printer, args=(), kwargs={})

foo_obj(bar=1)