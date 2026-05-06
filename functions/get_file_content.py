import os

from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        abs_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_path, file_path))

        if not os.path.commonpath([abs_path, target_path]) == abs_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_path, "r") as file:
            file_content_string = file.read(MAX_CHARS)
            if file.read(1):
                file_content_string += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        return file_content_string
    except Exception as e:
        return f"Error accessing file: {e}"


# AI Function Schema Declaration
schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "returns the content of a file given a file path relative to the working directory, truncating the result if over a certain amount of characters",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "str",
                    "description": "Directory path to file that needs its contents retrieved, relative to working directory",
                }
            },
            "required": ["file_path"],
        },
    },
}
