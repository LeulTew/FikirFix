from functions.run_python import run_python_file


if __name__ == "__main__":
    print(run_python_file("calculator", "main.py"))
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print(run_python_file("calculator", "tests.py"))
    print(run_python_file("calculator", "../main.py"))
    print(run_python_file("calculator", "nonexistent.py"))
from functions.run_python import run_python_file


if __name__ == "__main__":
    print("Case: calculator main.py (no args)")
    print(run_python_file("calculator", "main.py"))
    print()

    print("Case: calculator main.py (with args)")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print()

    print("Case: calculator tests.py")
    print(run_python_file("calculator", "tests.py"))
    print()

    print("Case: execute ../main.py (outside)")
    print(run_python_file("calculator", "../main.py"))
    print()

    print("Case: nonexistent file")
    print(run_python_file("calculator", "nonexistent.py"))
