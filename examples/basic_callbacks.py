from reactive import _

def printer(trace, message='Hello', *args, **kwargs):
  print 'Message: ' + str(message)
  print 'Trace: ' + str(trace) 
  print 'Args: ' + str(args)
  print 'Kwargs: ' + str(kwargs)
 
obj = _(1)

obj.onchange(printer, args=(), kwargs={'message': 'Test'})

obj += 1