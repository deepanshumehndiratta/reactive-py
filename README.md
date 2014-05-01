# Reactive-Py

A Python library to overload the basic [Data-Model](https://docs.python.org/2/reference/datamodel.html) to convert it to reactive data structures making it possible to fuse [reactive programming](http://en.wikipedia.org/wiki/Reactive_programming) with ordinary imperative programming for:

 * On-Change Callbacks
 * On-Compare Callbacks
 * Pre and Post filters for function calls


Data-structures supported (user-defined):

 * str
 * int
 * float
 * bool
 * list
 * tuples
 * dict
 * functions/methods
 * classes
 
### Importing the module

```python
from reactive import _
```

### On-Change Callbacks

#### Basic Callbacks (Asynchronous)

```python
def printer(trace, message='Hello', *args, **kwargs):
  print 'Message: ' + str(message)
  print 'Trace: ' + str(trace) 
  print 'Args: ' + str(args)
  print 'Kwargs: ' + str(kwargs)
 
obj = _(1)

obj.onchange(printer, args=(), kwargs={'message': 'Test'})

obj += 1

```

Output:

```bash
Message: Test
Trace: {'after_value': 2, 'before_value': 1, 'after_type': <type 'int'>, 'event': '__iadd__', 'before_type': <type 'int'>}
Args: ()
Kwargs: {}
[Finished in 0.1s]
```

(By default a callback is Asynchronous 

#### Synchronous Callbacks

```python
import time

def printer(trace, message='Hello', *args, **kwargs):
  time.sleep(2)
  print 'Message: ' + str(message)
 
obj = _("Hello")

obj.onchange(printer, args=(), kwargs={'message': 'Test'}, async=False)

obj += " World"

print "Here!"
```

Output:

```bash
Message: Test
Here!
[Finished in 2.1s]
```

#### Chaining Callbacks

```python
def printer(trace, message='Hello', *args, **kwargs):
  print 'Message: ' + str(message)

def hello_world(trace, name='Deepanshu', *args, **kwargs):
  print 'Hello ' + name + '!'
 
obj = _("Hello")

obj.onchange(printer, args=(), kwargs={'message': "Test"})\
  .onchange(hello_world, args=(), kwargs={})

obj += " World"
```

Output:

```bash
Message: Test
Hello Deepanshu!
[Finished in 0.1s]
```

### On-compare Callbacks

```python
def printer(trace, *args, **kwargs):
  print 'Trace: ' + str(trace)
 
obj = _("Hello")

obj.oncompare(printer, args=(), kwargs={})

obj == " World"
```

Output:

```bash
Trace: {'after_type': <type 'str'>, 'before_type': <type 'str'>, 'after_value': ' World', 'comparison_output': False, 'before_value': 'Hello', 'event': '__eq__'}
[Finished in 0.1s]
```

### Function callbacks

#### Before Function-Call Callback

```python
def foo(bar=None, baz=None):
  print 'bar: ' + str(bar)
  print 'baz: ' + str(baz)

def printer(trace, *args, **kwargs):
  print 'Trace: ' + str(trace)
 
foo_obj = _(foo)

foo_obj.before_call(printer, args=(), kwargs={})

foo_obj(bar=1)
```

Output:

```bash
bar: 1
baz: None
Trace: {'kwargs': {'bar': 1}, 'args': (), 'event': '__call__', 'before_call': True}
[Finished in 0.1s]
```

#### After Function-Call Callback

```python
def foo(bar=None, baz=None):
  print 'bar: ' + str(bar)
  print 'baz: ' + str(baz)
  return "Return Value"

def printer(trace, *args, **kwargs):
  print 'Trace: ' + str(trace)
 
foo_obj = _(foo)

foo_obj.after_call(printer, args=(), kwargs={})

foo_obj(bar=1)
```

Output:

```bash
bar: 1
baz: None
Trace: {'kwargs': {'bar': 1}, 'args': (), 'output': 'Return Value', 'event': '__call__', 'after_call': True}
[Finished in 0.1s]
```

### Assigning values to reactive objects

In Python, assignment is a [language intrinsic](http://docs.python.org/reference/simple_stmts.html#grammar-token-assignment_stmt) which doesn't have a modification hook. Which means, it can't be overloaded like the other Arithemetic or Logical operators.

	A hack around this would be to inspect the stack at every tick and call the respective hooks accordingly. This however, isn't an ideal way to do it and acts as a major bottleneck in program execution.

However, to truly make the python object "reactive", assignment is done in the following way:

```python
def foo(trace, *args, **kwargs):
  print 'Trace: ' + str(trace)

# Create a new reactive <'type' int> object
obj = _(1)

obj.onchange(foo, args=(), kwargs={})

# Assign value 2 to the object while keeping all its hooks (onchange, oncompare, before_call, after_call, etc) if any, intact and trigger a onchange event simultaneously
 
obj._(2)
```
Output:

```bash
Trace: {'after_value': 2, 'before_value': 1, 'after_type': <type 'int'>, 'event': '__assignment__', 'before_type': <type 'int'>}
[Finished in 0.1s]
```

### Working with lists

```python
def foo(trace, *args, **kwargs):
  print 'Trace: ' + str(trace)

# Create a new reactive list
obj = _([1, 2, 3, 4, 5])

obj.onchange(foo, args=(), kwargs={})
 
obj[2] = 4
```

Output:

```bash
Trace: {'index': 2, 'after_type': <type 'int'>, 'before_type': <type 'int'>, 'after_value': 4, 'before_value': 3, 'event': '__setitem__'}
[Finished in 0.1s]
```

### Working with tuples

```python
def foo(trace, *args, **kwargs):
  print 'Trace: ' + str(trace)

# Create a new reactive tuple
obj = _(('a', 'b'))

obj.onchange(foo, args=(), kwargs={})
 
obj += ('c', 'd')
```

Output:

```bash
Trace: {'after_value': ('a', 'b', 'c', 'd'), 'before_value': ('a', 'b'), 'after_type': <type 'tuple'>, 'event': '__iadd__', 'before_type': <type 'tuple'>}
[Finished in 0.1s]
```

### Working with dicts

```python
def foo(trace, *args, **kwargs):
  print 'Trace: ' + str(trace)

# Create a new reactive dict
obj = _({'a': 'b', 'c': 'd'})

obj.onchange(foo, args=(), kwargs={})
 
obj['e'] = 'f'
```

Output:

```bash
Trace: {'index': 'e', 'after_type': <type 'str'>, 'before_type': <type 'NoneType'>, 'after_value': 'f', 'before_value': None, 'event': '__setitem__'}
[Finished in 0.1s]
```

### Working with classes

```python
def foo(trace, *args, **kwargs):
  print 'Trace: ' + str(trace)

class A:
  pass

# Create a new reactive <'type' int> object
obj = _(A())

obj.onchange(foo, args=(), kwargs={})
 
obj.a = 'B'
obj.a = 'C'
```

Output:

```bash
Trace: {'attr': 'a', 'after_type': <type 'str'>, 'before_type': <type 'NoneType'>, 'after_value': 'B', 'before_value': None, 'event': '__setattr__'}
Trace: {'attr': 'a', 'after_type': <type 'str'>, 'before_type': <type 'str'>, 'after_value': 'C', 'before_value': 'B', 'event': '__setattr__'}
[Finished in 0.1s]
```

### Supported Operators

 * [Python Basic Operators](http://www.tutorialspoint.com/python/python_basic_operators.htm)


### License

The MIT License (MIT)

Copyright (c) 2014 Deepanshu Mehndiratta
