import os

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_working_directory = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)

        if not abs_full_path.startswith(abs_working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(abs_full_path, "r") as f:
            content = f.read(MAX_CHARS)
            if len(content) == MAX_CHARS:
                content += f' [...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except (OSError, PermissionError) as e:
        return f"Error: {str(e)}"

schema_get_file_content = {
    "name": "get_file_content",
    "description": "Reads the content of a file, constrained to the working directory. Truncates if longer than 10000 characters.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The relative path to the file within the working directory."
            }
        },
        "required": ["file_path"]
    }
}