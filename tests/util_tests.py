import difflib


def print_diff(expected, actual):
    expected_lines = expected.splitlines(keepends=True)
    actual_lines = actual.splitlines(keepends=True)
    diff = difflib.unified_diff(expected_lines, actual_lines, fromfile='expected', tofile='actual')
    for line in diff:
        print(line, end='')

    print("-" * 50)

    print("Actual:")
    print(actual)
    print("-"*50)
    print("Expected:")
    print(expected)
