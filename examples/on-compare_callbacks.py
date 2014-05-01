from reactive import _

def printer(trace, *args, **kwargs):
  print 'Trace: ' + str(trace)
 
obj = _("Hello")

obj.oncompare(printer, args=(), kwargs={})

obj == " World"