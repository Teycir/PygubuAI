"""Convert tkinter code to pygubu format"""
import sys
from pathlib import Path



def main():
    """CLI entry point for tkinter-to-pygubu converter"""
    if len(sys.argv) != 2:
        print("Usage: tkinter-to-pygubu <file>.py")
        print("\nConverts legacy tkinter code to pygubu format")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"Error: {filepath} not found")
        sys.exit(1)

    print(f"Converting {filepath.name} to Pygubu format...")
    print("\nWARNING  This is a placeholder implementation.")
    print("Full conversion requires parsing tkinter widget creation code.")
    print("\nSuggested approach:")
    print("1. Manually recreate UI in pygubu-designer")
    print("2. Copy business logic to new pygubu app class")
    print("3. Connect callbacks via builder.connect_callbacks()")


if __name__ == '__main__':
    main()
