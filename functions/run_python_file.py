import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    try:
        abs_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_path, file_path))

        if not os.path.commonpath([abs_path, target_path]) == abs_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file.'
        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_path]
        if args is not None:
            command.extend(args)
        result = subprocess.run(
            command, cwd=abs_path, capture_output=True, text=True, timeout=30
        )

        output = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        return "\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "returns the stdout and stderr of a .py file path after executing it, relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "str",
                    "description": "Directory path to python file that needs to be executed, relative to working directory",
                },
                "args": {
                    "type": "arr",
                    "description": "Optional additional arguments to pass to the python file when executing it, in an array. If the user doesn't specify any arguments, don't add any",
                    "items": {
                        "type": "str",
                        "description": "The items of the args array, in string format",
                    },
                },
            },
            "required": ["file_path"],
        },
    },
}
