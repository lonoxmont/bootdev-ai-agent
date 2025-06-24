import os
from google.genai import types
def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    target = os.path.abspath(os.path.join(working_directory, file_path))
    if not target.startswith(abs_working_dir):
        return f"Error: Cannot write to '{file_path}' as it is outside the permitted working directory"
    if not os.path.exists(target):
        try:
            os.makedirs(os.path.dirname(target), exist_ok=True)
        except Exception as e:
            return f"Error: {e}"
    try:
        with open(target, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error writing to {file_path}: {e}"
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents to be written to the previously specified file."
            )
        },
    ),
)
