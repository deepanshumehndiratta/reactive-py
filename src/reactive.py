'''
  @module: Reactive-Py
  @license: MIT
  @author: Deepanshu Mehndiratta
  @email: deepanshumehndiratta [at] gmail [dot] com
'''
from __future__ import division
from threading import Thread
from copy import deepcopy
import sys, collections

class _(object):

  '''
  __on<event> = {'async': [{'func': None, 'args': (), 'kwargs': {}}],
                'sync': [{'func': None, 'args': (), 'kwargs': {}}]}
  '''
  __onchange = {'sync': [], 'async': []}
  __oncompare = {'sync': [], 'async': []}
  __before_call = {'sync': [], 'async': []}
  __after_call = {'sync': [], 'async': []}
  __log_events = False

  '''
    ---------------------------------
    Initialization of Reactive Object
    ---------------------------------
  '''

  def __init__(self, data):
    self.__initialize(data)

  def _(self, data):
    temp = deepcopy(self.__data)
    self.__initialize(data)
    self.__trigger('__assignment__', trace={'before_type': type(temp),\
     'before_value': temp, 'after_type': type(self.__data), 'after_value':  self.__data})
    return self

  def __initialize(self, data):
    if data is not None:
      '''
      if isinstance(data, list):
        self.__data = [_(d) for d in data]
        print self.__data
      elif isinstance(data, tuple):
        self.__data = (_(d) for d in data)
      elif isinstance(data, dict):
        self.__data = {k:_(v) for k,v in data.iteritems()}
      else:
        self.__data = data
      '''
      self.__data = data
    else:
      raise Exception("Please initialize the variable with data.")

  '''
    ---------------------
    Event binding methods
    ---------------------
  '''

  def __trigger(self, event, *args, **kwargs):

    trace = kwargs.get('trace', {})
    trace['event'] = event
    before_type = trace.get('before_type',None)
    before_value = trace.get('before_value',None)
    after_type = trace.get('after_type',None)
    after_value = trace.get('after_value',None)
    before_call = trace.get('before_call',False)
    after_call = trace.get('after_call',False)
    comparison_output = trace.get('comparison_output',False)
    func_args = trace.get('args',())
    func_kwargs = trace.get('kwargs',{})
    func_output = trace.get('output',None)
    
    change_events = ['__assignment__', '__iadd__', '__isub__', '__imul__', '__idiv__', '__itruediv__',\
     '__ifloordir__', '__ipow__', '__iand__', '__ior__', '__ixor__', '__invert__',\
      '__ilshift__', '__irshift__', '__setitem__', '__delitem__', 'append', 'extend',\
      'insert', 'pop', 'remove', 'reverse', 'sort', 'clear', 'setdefault', 'update', '__setattr__']
    compare_events = ['__lt__', '__gt__', '__le__', '__ge__', '__eq__', '__ne__']
    
    if event in change_events:

      message = "%s with value %s changed to %s with value %s using %s" %\
                  (before_type, before_value, after_type, after_value,\
                    event)
      Thread(target=self.__log, kwargs={'message': message,\
        'trace': trace, 'event': event}).start()

      '''
        Trigger onchange event
      '''
      # Asynchronous callbacks
      for callback in self.__onchange['async']:
        if isinstance(callback['func'], collections.Callable):
          self.__async_callback(callback['func'], *callback['args'],\
            **dict({'trace': trace}.items() + callback['kwargs'].items()))
      # Synchronous callbacks
      for callback in self.__onchange['sync']:
        if isinstance(callback['func'], collections.Callable):
          self.__sync_callback(callback['func'], *callback['args'],\
            **dict({'trace': trace}.items() + callback['kwargs'].items()))

    elif event in compare_events:

      message = "%s with value %s compared with %s with value %s using %s with result %s" %\
                  (before_type, before_value, after_type, after_value,\
                    event, str(comparison_output))
      Thread(target=self.__log, kwargs={'message': message,\
        'trace': trace, 'event': event}).start()

      '''
        Trigger oncompare event
      '''
      # Asynchronous callbacks
      for callback in self.__oncompare['async']:
        if isinstance(callback['func'], collections.Callable):
          self.__async_callback(callback['func'], *callback['args'],\
            **dict({'trace': trace}.items() + callback['kwargs'].items()))
      # Synchronous callbacks
      for callback in self.__oncompare['sync']:
        if isinstance(callback['func'], collections.Callable):
          self.__sync_callback(callback['func'], *callback['args'],\
            **dict({'trace': trace}.items() + callback['kwargs'].items()))

    elif event == '__call__':
      # Before function-call callback
      if before_call:

        message = "Before function called for %s with args: %s and kwargs: %s" %\
                    (self.__data.__name__, func_args, func_kwargs)
        Thread(target=self.__log, kwargs={'message': message,\
          'trace': trace, 'event': event}).start()

        '''
          Trigger before_call event
        '''
        # Asynchronous callbacks
        for callback in self.__before_call['async']:
          if isinstance(callback['func'], collections.Callable):
            self.__async_callback(callback['func'], *callback['args'],\
              **dict({'trace': trace}.items() + callback['kwargs'].items()))
        # Synchronous callbacks
        for callback in self.__before_call['sync']:
          if isinstance(callback['func'], collections.Callable):
            self.__sync_callback(callback['func'], *callback['args'],\
              **dict({'trace': trace}.items() + callback['kwargs'].items()))

      elif after_call:

        message = "After function called for %s with args: %s and kwargs: %s with result %s" %\
                    (self.__data.__name__, func_args, func_kwargs, func_output)
        Thread(target=self.__log, kwargs={'message': message,\
          'trace': trace, 'event': event}).start()

        '''
          Trigger before_call event
        '''
        # Asynchronous callbacks
        for callback in self.__after_call['async']:
          if isinstance(callback['func'], collections.Callable):
            self.__async_callback(callback['func'], *callback['args'],\
              **dict({'trace': trace}.items() + callback['kwargs'].items()))
        # Synchronous callbacks
        for callback in self.__after_call['sync']:
          if isinstance(callback['func'], collections.Callable):
            self.__sync_callback(callback['func'], *callback['args'],\
              **dict({'trace': trace}.items() + callback['kwargs'].items()))

  def __log(self, message, event, trace):
    if self.__log_events:
      print message
      print 'Trace for event ' + event + ': ' + str(trace)

  def logging(self, log=True):
    if type(log) == bool:
      self.__log_events = log

  def onchange(self, callback=None, *args, **kwargs):
    self.__onchange['async' if kwargs.get('async', True) else 'sync'].append({'func': callback,\
      'args': kwargs.get('args', ()), 'kwargs': kwargs.get('kwargs', {})})
    return self

  def oncompare(self, callback=None, *args, **kwargs):
    self.__oncompare['async' if kwargs.get('async', True) else 'sync'].append({'func': callback,\
      'args': kwargs.get('args', ()), 'kwargs': kwargs.get('kwargs', {})})
    return self

  def before_call(self, callback=None, *args, **kwargs):
    self.__before_call['async' if kwargs.get('async', True) else 'sync'].append({'func': callback,\
      'args': kwargs.get('args', ()), 'kwargs': kwargs.get('kwargs', {})})
    return self

  def after_call(self, callback=None, *args, **kwargs):
    self.__after_call['async' if kwargs.get('async', True) else 'sync'].append({'func': callback,\
      'args': kwargs.get('args', ()), 'kwargs': kwargs.get('kwargs', {})})
    return self

  '''
    ----------------------
    Mathematical operators
    ----------------------
  '''

  '''
    Addition (a + b, a += b, b + a)
  '''
  def __add__(self, x):
    return self.__data + x

  def __iadd__(self, x):
    temp = deepcopy(self.__data)
    self.__data += x
    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(temp),\
     'before_value': temp, 'after_type': type(self.__data), 'after_value':  self.__data})
    return self

  def __radd__(self, x):
    return x + self.__data

  '''
    Subtraction (a - b, a -= b, b - a)
  '''

  def __sub__(self, x):
    return self.__data - x

  def __isub__(self, x):
    temp = deepcopy(self.__data)
    self.__data -= x
    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(temp),\
     'before_value': temp, 'after_type': type(self.__data), 'after_value':  self.__data})
    return self

  def __rsub__(self, x):
    return x - self.__data

  '''
    Multiplication (a * b, a *= b, b * a)
  '''

  def __mul__(self, x):
    return self.__data * x

  def __imul__(self, x):
    temp = deepcopy(self.__data)
    self.__data *= x
    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(temp),\
     'before_value': temp, 'after_type': type(self.__data), 'after_value':  self.__data})
    return self

  def __rmul__(self, x):
    return x * self.__data

  '''
    Division (a / b, a /= b, b / a)
  '''

  def __div__(self, x):
    return self.__data / x

  def __idiv__(self, x):
    temp = deepcopy(self.__data)
    self.__data /= x
    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(temp),\
     'before_value': temp, 'after_type': type(self.__data), 'after_value':  self.__data})
    return self

  def __rdiv__(self, x):
    return x / self.__data

  '''
    True Division (Floating point) (a / b, a /= b, b / a)
  '''

  def __truediv__(self, x):
    return self.__data / x

  def __itruediv__(self, x):
    temp = deepcopy(self.__data)
    self.__data /= x
    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(temp),\
     'before_value': temp, 'after_type': type(self.__data), 'after_value':  self.__data})
    return self

  def __rtruediv__(self, x):
    return x / self.__data

  '''
    Floor Division (a // b, a //= b, b // a)
  '''

  def __floordiv__(self, x):
    return self.__data // x

  def __ifloordiv__(self, x):
    temp = deepcopy(self.__data)
    self.__data //= x
    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(temp),\
     'before_value': temp, 'after_type': type(self.__data), 'after_value':  self.__data})
    return self

  def __rfloordiv__(self, x):
    return x // self.__data

  '''
    Power (a ** b, a **= b, b ** a)
  '''

  def __pow__(self, x):
    return self.__data ** x

  def __ipow__(self, x):
    temp = deepcopy(self.__data)
    self.__data **= x
    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(temp),\
     'before_value': temp, 'after_type': type(self.__data), 'after_value':  self.__data})
    return self

  def __rpow__(self, x):
    return x ** self.__data

  '''
    --------------------
    Comparison Operators
    --------------------
  '''

  def __lt__(self, x):
    temp = deepcopy(self.__data) < x
    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(self.__data),\
     'before_value': self.__data, 'after_type': type(x), 'after_value': x, 'comparison_output': temp})
    return temp

  def __gt__(self, x):
    temp = deepcopy(self.__data) > x
    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(self.__data),\
     'before_value': self.__data, 'after_type': type(x), 'after_value': x, 'comparison_output': temp})
    return temp

  def __le__(self, x):
    temp = deepcopy(self.__data) <= x
    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(self.__data),\
     'before_value': self.__data, 'after_type': type(x), 'after_value': x, 'comparison_output': temp})
    return temp

  def __ge__(self, x):
    temp = deepcopy(self.__data) >=x
    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(self.__data),\
     'before_value': self.__data, 'after_type': type(x), 'after_value': x, 'comparison_output': temp})
    return temp

  def __eq__(self, x):
    temp = deepcopy(self.__data) == x
    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(self.__data),\
     'before_value': self.__data, 'after_type': type(x), 'after_value': x, 'comparison_output': temp})
    return temp

  def __ne__(self, x):
    temp = deepcopy(self.__data) != x
    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(self.__data),\
     'before_value': self.__data, 'after_type': type(x), 'after_value': x, 'comparison_output': temp})
    return temp

  '''
    -----------------
    Bitwise operators
    -----------------
  '''

  '''
    AND (a & b, a &= b, b & a)
  '''

  def __and__(self, x):
    return self.__data & x

  def __iand__(self, x):
    temp = deepcopy(self.__data)
    self.__data &= x
    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(temp),\
     'before_value': temp, 'after_type': type(self.__data), 'after_value':  self.__data})
    return self

  def __rand__(self, x):
    return x & self.__data

  '''
    OR (a | b, a |= b, b | a)
  '''

  def __or__(self, x):
    return self.__data | x

  def __ior__(self, x):
    temp = deepcopy(self.__data)
    self.__data |= x
    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(temp),\
     'before_value': temp, 'after_type': type(self.__data), 'after_value':  self.__data})
    return self

  def __ror__(self, x):
    return x | self.__data

  '''
    XOR (a ^ b, a ^= b, b ^ a)
  '''

  def __xor__(self, x):
    return self.__data ^ x

  def __ixor__(self, x):
    temp = deepcopy(self.__data)
    self.__data ^= x
    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(temp),\
     'before_value': temp, 'after_type': type(self.__data), 'after_value':  self.__data})
    return self

  def __rxor__(self, x):
    return x ^ self.__data

  '''
    INVERT (~ a)
  '''

  def __invert__(self):
    return ~ self.__data

  '''
    LSHIFT (a << b, a <<= b, b << a)
  '''

  def __lshift__(self, x):
    return self.__data << x

  def __ilshift__(self, x):
    temp = deepcopy(self.__data)
    self.__data <<= x
    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(temp),\
     'before_value': temp, 'after_type': type(self.__data), 'after_value':  self.__data})
    return self

  def __rlshift__(self, x):
    return x << self.__data

  '''
    RSHIFT (a >> b, a >>= b, b >> a)
  '''

  def __rshift__(self, x):
    return self.__data >> x

  def __irshift__(self, x):
    temp = deepcopy(self.__data)
    self.__data >>= x
    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(temp),\
     'before_value': temp, 'after_type': type(self.__data), 'after_value':  self.__data})
    return self

  def __rrshift__(self, x):
    return x >> self.__data

  '''
    ---------------
    Misc. operators
    ---------------
  '''

  def __iter__(self):
    return iter(self.__data)

  def __contains__(self, x):
    return True if x in self.__data else False

  def __len__(self, x):
    return len(self.__data)

  def __max__(self, x):
    return max(self.__data)

  def __min__(self, x):
    return min(self.__data)

  def __bool__(self, x):
    return bool(self.__value)

  def __get__(self, x):
    raise Exception("Attribute access denied.")

  def __set__(self, x):
    raise Exception("Attribute access denied.")
    
  def __delete__(self, x):
    raise Exception("Attribute access denied.")

  '''
    ------------
    List methods
    ------------
  '''

  def __getitem__(self, index):
    return self.__data[index]

  def __setitem__(self, index, value):
    temp = deepcopy(self.__data[index] if index in self.__data else None)
    self.__data[index] = value
    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(temp),\
     'before_value': temp, 'after_type': type(value), 'after_value': value, 'index': index})
    return self
    
  def __delitem__(self, index):
    assert index in self.__data
    temp = deepcopy(self.__data[index])
    del self.__data[index]
    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(temp),\
     'before_value': temp, 'index': index})

  def append(self, obj):
    temp = deepcopy(self.__data)
    self.__data.append(obj)
    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(temp),\
     'before_value': temp, 'after_type': type(self.__data), 'after_value':  self.__data})

  def count(self, obj):
    return self.__data.count(obj)

  def extend(self, seq):
    temp = deepcopy(self.__data)
    self.__data.extend(seq)
    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(temp),\
     'before_value': temp, 'after_type': type(self.__data), 'after_value':  self.__data})

  def index(self, obj):
    return self.__data.index(obj)

  def insert(self, index, obj):
    temp = deepcopy(self.__data)
    self.__data.insert(index, obj)
    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(temp),\
     'before_value': temp, 'after_type': type(self.__data), 'after_value': self.__data, 'index': index})

  def pop(self, obj):
    temp = deepcopy(self.__data)
    rtr = self.__data.pop(obj)
    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(temp),\
     'before_value': temp, 'after_type': type(self.__data), 'after_value': self.__data, 'obj': obj})
    return rtr

  def remove(self, obj):
    temp = deepcopy(self.__data)
    self.__data.remove(obj)
    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(temp),\
     'before_value': temp, 'after_type': type(self.__data), 'after_value': self.__data, 'obj': obj})

  def reverse(self):
    temp = deepcopy(self.__data)
    self.__data.reverse()
    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(temp),\
     'before_value': temp, 'after_type': type(self.__data), 'after_value':  self.__data})

  def sort(self, func=None):
    temp = deepcopy(self.__data)

    if func:
      self.__data.sort(func)
    else:
      self.__data.sort()

    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(temp),\
      'before_value': temp, 'after_type': type(self.__data), 'after_value': self.__data, 'sort_func': func})

  '''
    ------------------
    Dictionary methods
    ------------------
  '''

  def clear(self):
    temp = deepcopy(self.__data)
    self.__data.clear()
    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(temp),\
     'before_value': temp, 'after_type': type(self.__data), 'after_value':  self.__data})

  def copy(self):
    return self.__data.copy()

  def fromkeys(self, seq, value=None):
    if not value:
      return self.__data.fromkeys(seq)
    return self.__data.fromkeys(seq, value)

  def get(self, key, default=None):
    if not default:
      return self.__data.get(key)
    return self.__data.get(key, default)

  def has_key(self, key):
    return self.__data.has_key(key)

  def items(self):
    return self.__data.items()

  def keys(self):
    return self.__data.keys()

  def setdefault(self, key, default=None):
    if not default:
      return self.__data.setdefault(key)

    temp = deepcopy(self.__data)
    rtr = self.__data.setdefault(key, default)
    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(temp),\
     'before_value': temp, 'after_type': type(self.__data), 'after_value': self.__data,\
     'key': key, 'default': default})
    return rtr

  def update(self, dict2):
    temp = deepcopy(self.__data)
    self.__data.update(dict2)
    self.__trigger(sys._getframe().f_code.co_name, trace={'before_type': type(temp),\
     'before_value': temp, 'after_type': type(self.__data), 'after_value':  self.__data})

  def values(self):
    return self.__data.values()

  '''
    ----------------
    Function methods
    ----------------
  '''

  def __call__(self, *args, **kwargs):
    if isinstance(self.__data, collections.Callable):
      self.__trigger(sys._getframe().f_code.co_name, trace={'before_call': True,\
        'args': args, 'kwargs': kwargs})
      temp = self.__data(*args, **kwargs)
      self.__trigger(sys._getframe().f_code.co_name, trace={'after_call': True,\
        'args': args, 'kwargs': kwargs, 'output': temp})
      return temp
    else:
        raise TypeError('%s is not callable' % type(self.__data))

  '''
    ----------------
    Instance Methods
    ----------------
  '''
  
  def __setattr__(self, attr, value):
    if attr is None:
      return
    try:
      temp = None
      if attr != '__data':
        try:
          temp = deepcopy(super(_, self).__getattribute__(attr))
        except:
          pass
      super(_, self).__setattr__(attr, value)
      if attr != '__data':
        self.__trigger(sys._getframe().f_code.co_name, trace={'attr': attr,\
          'before_value': temp, 'before_type': type(temp), 'after_value': value,\
          'after_type': type(value)})
    except Exception,e:
      print str(e)

  def __getattr__(self, attr):
    if attr is None:
      return self.__data
    if self.__data is None:
      raise AttributeError('unreadable attribute')
    try:
      fget = getattr(self.__data, attr)
    except AttributeError:
      raise TypeError('%s object does not have a %s attribute' %
              (type(self.__data).__name__, self.__data))
    return fget

  '''
    ---------------------
    Object representation
    ---------------------
  '''

  def __repr__(self):
    return str(self.__data)

  def __str__(self):
    return str(self.__data)

  def __dir__(self):
    return dir(self.__data)

  '''
    ---------------
    Event callbacks
    ---------------
  '''

  def __sync_callback(self, callback, *args, **kwargs):
    callback(*args, **kwargs)

  def __async_callback(self, callback, *args, **kwargs):
    thread = Thread(target=callback, args=args, kwargs=kwargs)
    # Don't exit the program till all callbacks have executed successfully
    # thread.daemon = True
    thread.start()