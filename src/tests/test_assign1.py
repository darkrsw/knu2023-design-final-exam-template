from ..myfile import AnotherClass
from ..this import ThisClass

def test_AnotherClass():
    a = AnotherClass()
    a.func1()
    a.func2("aaa")
    a.func2([])

def test_ThisClass():
    b = ThisClass()
    b.func1("a", 1)
