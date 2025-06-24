import os
from google.genai import types

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target = os.path.abspath(os.path.join(working_directory, file_path))
    if not target.startswith(abs_working_dir):
        return f"Error: Cannot read '{file_path}' as it is outside the permitted working directory"
    if not os.path.isfile(target):
        return f"Error: File not found or is not a regular file: '{file_path}'"
    
    try:
        MAX_CHARS = 10000

        with open(target, "r") as f:
            file_content_string = f.read(MAX_CHARS + 1)
        if len(file_content_string) <= MAX_CHARS:
            return file_content_string
        if len(file_content_string) > MAX_CHARS:
            return file_content_string[0:MAX_CHARS] + f'[...File "{file_path}" truncated at 10000 characters]'
    except Exception as e:
        return f"Error: Error opening file: {e}"
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read from, relative to the working directory.",
            ),
        },
    ),
)
