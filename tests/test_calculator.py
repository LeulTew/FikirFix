from calculator.pkg.calculator import Calculator


def test_calculator_precedence():
    c = Calculator()
    assert c.evaluate("3 + 7 * 2") == 17


def test_calculator_parentheses():
    c = Calculator()
    assert c.evaluate("(3 + 7) * 2") == 20


def test_calculator_float():
    c = Calculator()
    assert abs(c.evaluate("3.5 + 1.25") - 4.75) < 1e-9
