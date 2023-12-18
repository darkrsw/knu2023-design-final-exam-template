from analyzer import collect_variable_types

test_input_path = "./src"

def test1():
    expected = {'a': {'list', 'str', 'int'}}

    result = collect_variable_types(test_input_path, "AnotherClass")
    assert expected == result

def test2():
    expected = {'member1': {'int', 'str'}, 'member2': {'str'}, 'member3': {'int'}}

    result = collect_variable_types(test_input_path, "ThisClass")
    assert expected == result
