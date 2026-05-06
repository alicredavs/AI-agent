import json

from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import schema_write_file, write_file

tools = [
    schema_get_file_content,
    schema_get_files_info,
    schema_run_python_file,
    schema_write_file,
]


def call_function(tool_call, verbose=False):
    tool_name = tool_call.function.name or ""

    if verbose:
        print(f"Calling function: {tool_name}({tool_call.function.arguments})")
    else:
        print(f" - Calling function: {tool_name}")

    function_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    if tool_name not in function_map:
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": {"error": f"Unknown function: {tool_name}"},
        }

    arguments = (
        json.loads(tool_call.function.arguments)
        if tool_call.function.arguments.strip()
        else {}
    )
    arguments["working_directory"] = "./calculator"

    function_result = function_map[tool_name](**arguments)

    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": json.dumps(function_result),
    }
