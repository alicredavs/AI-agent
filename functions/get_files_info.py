import os


def get_files_info(working_directory, directory="."):
    try:
        abs_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_path, directory))

        if not os.path.commonpath([abs_path, target_path]) == abs_path:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_path):
            return f'Error: "{directory}" is not a directory'

        contents = []
        for item in os.listdir(target_path):
            filepath = os.path.join(target_path, item)
            is_dir = os.path.isdir(filepath)
            file_size = os.path.getsize(filepath)
            contents.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(contents)
    except Exception as e:
        return f"Error listing files: {e}"


# AI Function Schema Declaration
schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "str",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                }
            },
        },
    },
}
