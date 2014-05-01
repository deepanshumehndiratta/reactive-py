from reactive import _

def printer(trace, message='Hello', *args, **kwargs):
  print 'Message: ' + str(message)

def hello_world(trace, name='Deepanshu', *args, **kwargs):
  print 'Hello ' + name + '!'
 
obj = _("Hello")

obj.onchange(printer, args=(), kwargs={'message': "Test"})\
  .onchange(hello_world, args=(), kwargs={})

obj += " World"