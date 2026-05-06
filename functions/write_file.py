import os


def write_file(working_directory, file_path, content):
    try:
        abs_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_path, file_path))

        if not os.path.commonpath([abs_path, target_path]) == abs_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        with open(target_path, "w") as file:
            file.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: {e}"


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Takes a file path and content, then writes the content to the file specified in file path, relative to working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "str",
                    "description": "Directory path to file that needs to be written to, relative to working directory",
                },
                "content": {
                    "type": "str",
                    "description": "The content that needs to be written to a file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}
