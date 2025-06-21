import os

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
