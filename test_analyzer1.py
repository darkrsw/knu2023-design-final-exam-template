from analyzer import collect_variable_types

test_input_path = "./src"

def test1():
    expected = {}

    result = collect_variable_types(test_input_path, "")
    assert expected == result
