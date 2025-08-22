

def load_text_file_as_string(text_file_path):
    try:
        with open(text_file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
        print("File content successfully read into a string:")
        return file_content
    except FileNotFoundError:
        print("Error: The file 'your_file.txt' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")