from analyzer import collect_uninvoked_methods

test_input_path = "./src"

def test1():
    expected = {}

    result = collect_uninvoked_methods(test_input_path, "")
    assert expected == result
