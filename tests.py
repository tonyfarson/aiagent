from functions.get_file_content import get_file_content

def main():
    # Test case 1: main.py
    print("Result for main.py:")
    print(get_file_content("calculator", "main.py"))

    # Test case 2: pkg/calculator.py
    print("\nResult for pkg/calculator.py:")
    print(get_file_content("calculator", "pkg/calculator.py"))

    # Test case 3: /bin/cat (outside directory)
    print("\nResult for /bin/cat:")
    print(get_file_content("calculator", "/bin/cat"))

    # Test case 4: pkg/does_not_exist.py (non-existent file)
    print("\nResult for pkg/does_not_exist.py:")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))

if __name__ == "__main__":
    main()