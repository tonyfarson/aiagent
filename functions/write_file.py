import os

def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_working_directory = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)

        if not abs_full_path.startswith(abs_working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        dir_name = os.path.dirname(abs_full_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        with open(abs_full_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except (OSError, PermissionError) as e:
        return f"Error: {str(e)}"

schema_write_file = {
    "name": "write_file",
    "description": "Writes or overwrites the content of a file, constrained to the working directory.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The relative path to the file within the working directory."
            },
            "content": {
                "type": "string",
                "description": "The content to write to the file."
            }
        },
        "required": ["file_path", "content"]
    }
}