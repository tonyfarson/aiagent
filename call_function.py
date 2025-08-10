# No 'genai' import needed here anymore
import google.generativeai.types as types
from google.generativeai.types import Tool

# Import the actual functions and their schemas
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python import run_python_file, schema_run_python_file


WORKING_DIRECTORY = "./calculator"

function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}


def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    args = dict(function_call_part.args)

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    if function_name not in function_map:
        # Return a dictionary instead of a Content object
        return {
            "role": "tool",
            "parts": [{
                "function_response": {
                    "name": function_name,
                    "response": {"error": f"Unknown function: {function_name}"},
                }
            }],
        }

    args["working_directory"] = WORKING_DIRECTORY
    selected_function = function_map[function_name]
    function_result = selected_function(**args)

    # Return a dictionary instead of a Content object
    return {
        "role": "tool",
        "parts": [{
            "function_response": {
                "name": function_name,
                "response": {"result": function_result},
            }
        }],
    }


available_functions = Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)