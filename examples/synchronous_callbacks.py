from reactive import _
import time

def printer(trace, message='Hello', *args, **kwargs):
  time.sleep(2)
  print 'Message: ' + str(message)
 
obj = _("Hello")

obj.onchange(printer, args=(), kwargs={'message': 'Test'}, async=False)

obj += " World"

print "Here!"