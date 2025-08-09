import os

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    try:
        # Create the full path using os.path.join
        full_path = os.path.join(working_directory, file_path)
        # Get absolute paths for comparison
        abs_working_directory = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)

        # Check if the file is outside the working directory
        if not abs_full_path.startswith(abs_working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check if the path is a regular file
        if not os.path.isfile(abs_full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read the file contents, truncating if necessary
        with open(abs_full_path, "r") as f:
            content = f.read(MAX_CHARS)
            if len(content) == MAX_CHARS:
                content += f' [...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except (OSError, PermissionError) as e:
        return f"Error: {str(e)}"