from ..myfile import AnotherClass
from ..this import ThisClass

def test1():
    a = AnotherClass()
    a.func1()
    a.func2("aaa")
    a.func2([])

def test2():
    b = ThisClass()
    b.func1("a", 1)
