import os

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
        abs_working_directory = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)

        if not abs_full_path.startswith(abs_working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(abs_full_path):
            return f'Error: "{directory}" is not a directory'

        result = []
        for entry in os.listdir(abs_full_path):
            if entry == "__pycache__":
                continue
            entry_path = os.path.join(abs_full_path, entry)
            is_dir = os.path.isdir(entry_path)
            try:
                file_size = os.path.getsize(entry_path)
            except (OSError, PermissionError) as e:
                return f"Error: Unable to get size for {entry}: {str(e)}"
            result.append(f"- {entry}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(result) if result else "Error: Directory is empty"

    except (OSError, PermissionError) as e:
        return f"Error: {str(e)}"

schema_get_files_info = {
    "name": "get_files_info",
    "description": "Lists files in the specified directory along with their sizes, constrained to the working directory.",
    "parameters": {
        "type": "object",
        "properties": {
            "directory": {
                "type": "string",
                "description": "The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself."
            }
        }
    }
}