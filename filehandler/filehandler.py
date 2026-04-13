import os

class FileHandlerError(Exception):
    """Custom exception for File Handler operations."""
    pass

def validate_file(file_name, must_exist=True):
    """Checks if the filename is valid and if it exists."""
    if not file_name.strip():
        raise FileHandlerError("Filename cannot be empty.")
    if must_exist and not os.path.exists(file_name):
        raise FileNotFoundError(f"The file '{file_name}' does not exist.")

def write_to_file(file_name, content, mode='a'):
    """Appends or writes new content to the file with enhanced error handling."""
    try:
        validate_file(file_name, must_exist=(mode == 'a'))
        with open(file_name, mode) as file:
            file.write(content + "\n")
        print(f"[OK] Successfully {'appended to' if mode == 'a' else 'written to'} {file_name}!")
    except FileHandlerError as e:
        print(f"[ERROR] Validation failed: {e}")
    except PermissionError:
        print("[ERROR] Permission denied: Cannot write to this file.")
    except Exception as e:
        print(f"[ERROR] Unexpected error writing to file: {e}")

def find_and_replace(file_name, old_word, new_word):
    """Replaces words in the file with better validation."""
    try:
        if not old_word:
            raise FileHandlerError("The word to find cannot be empty.")
        
        validate_file(file_name)
        with open(file_name, 'r') as file:
            content = file.read()

        if old_word not in content:
            print(f"[WARN] The word '{old_word}' was not found in the file.")
            return

        updated_content = content.replace(old_word, new_word)

        with open(file_name, 'w') as file:
            file.write(updated_content)

        print("[OK] Word replaced successfully!")

    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
    except FileHandlerError as e:
        print(f"[ERROR] {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")

def string_manipulation(file_name):
    """Provides various string manipulation operations on file content."""
    try:
        validate_file(file_name)
        with open(file_name, 'r') as file:
            content = file.read()
        
        if not content.strip():
            print("[WARN] File is empty. Nothing to manipulate.")
            return

        print("\n--- String Manipulation Options ---")
        print("1. Word & Character Count")
        print("2. Convert to Uppercase")
        print("3. Convert to Lowercase")
        print("4. Reverse Content")
        
        sub_choice = input("Select operation (1-4): ")
        
        if sub_choice == '1':
            words = content.split()
            print(f"[INFO] Word Count: {len(words)}")
            print(f"[INFO] Character Count (with spaces): {len(content)}")
        elif sub_choice == '2':
            new_content = content.upper()
            save_manipulation(file_name, new_content)
        elif sub_choice == '3':
            new_content = content.lower()
            save_manipulation(file_name, new_content)
        elif sub_choice == '4':
            new_content = content[::-1]
            save_manipulation(file_name, new_content)
        else:
            print("[ERROR] Invalid sub-choice.")

    except Exception as e:
        print(f"[ERROR] Manipulation failed: {e}")

def save_manipulation(file_name, content):
    """Helper to save manipulated content back to the file."""
    try:
        with open(file_name, 'w') as file:
            file.write(content)
        print("[OK] File content updated with string manipulation!")
    except Exception as e:
        print(f"[ERROR] Failed to save changes: {e}")

def main():
    print("--- Advanced File Handler App ---")
    
    try:
        file_name = input("Enter the filename (e.g., sample.txt): ").strip()
        validate_file(file_name, must_exist=False) # Check filename validity, don't require it to exist yet

        while True:
            print("\nChoose an action:")
            print("1. Write/Append text to file")
            print("2. Find and Replace text")
            print("3. String Manipulation (Count, Case, Reverse)")
            print("4. Exit")
            
            choice = input("Enter choice (1-4): ")
            
            if choice == '1':
                text = input("Enter text to add: ")
                write_to_file(file_name, text)
            elif choice == '2':
                old_word = input("Enter the word to find: ")
                new_word = input("Enter the replacement word: ")
                find_and_replace(file_name, old_word, new_word)
            elif choice == '3':
                string_manipulation(file_name)
            elif choice == '4':
                print("Goodbye!")
                break
            else:
                print("[ERROR] Invalid choice, please try again.")
    
    except FileHandlerError as e:
        print(f"[ERROR] Setup failed: {e}")
    except KeyboardInterrupt:
        print("\n[INFO] Program stopped by user.")
    except Exception as e:
        print(f"[ERROR] A critical error occurred: {e}")

if __name__ == "__main__":
    main()
