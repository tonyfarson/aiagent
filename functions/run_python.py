import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_working_directory = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)

        if not abs_full_path.startswith(abs_working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(abs_full_path):
            return f'Error: File "{file_path}" not found.'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        completed_process = subprocess.run(
            ['python', abs_full_path] + args,
            timeout=30,
            capture_output=True,
            text=True,
            cwd=abs_working_directory
        )

        output = []
        if completed_process.stdout:
            output.append(f"STDOUT:\n{completed_process.stdout.strip()}")
        if completed_process.stderr:
            output.append(f"STDERR:\n{completed_process.stderr.strip()}")
        if completed_process.returncode != 0:
            output.append(f"Process exited with code {completed_process.returncode}")

        if output:
            return "\n\n".join(output)
        else:
            return "No output produced."

    except subprocess.TimeoutExpired:
        return "Error: Execution timed out after 30 seconds."
    except (OSError, PermissionError, subprocess.SubprocessError) as e:
        return f"Error: executing Python file: {str(e)}"

schema_run_python_file = {
    "name": "run_python_file",
    "description": "Executes a Python file in the working directory with optional arguments and a 30-second timeout, capturing stdout and stderr.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The relative path to the Python file within the working directory."
            },
            "args": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Optional command-line arguments to pass to the Python file."
            }
        },
        "required": ["file_path"]
    }
}