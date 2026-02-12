def inputMenu(prompt: str, options: list) -> int:
    """Displays a menu with the given prompt and options, and returns the user's choice as an integer."""
    while True:
        print(prompt)
        for i, option in enumerate(options, 1):
            print(f"{i} - {option}")
        choice = input("Enter your choice: ")
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return int(choice)
        else:
            print("Invalid choice. Please try again.")
