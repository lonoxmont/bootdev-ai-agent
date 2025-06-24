import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    abs_working_dir = os.path.abspath(working_directory)
    target = os.path.abspath(os.path.join(working_directory, file_path))
    if os.path.commonpath([abs_working_dir, target]) != abs_working_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory.'
    if not os.path.isfile(target):
        return f'Error: File "{file_path}" not found.'
    if not target.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        commands = ["python3", target]
        if args:
            commands.extend(args)
        result = subprocess.run(
            commands,
            text=True,
            cwd=abs_working_dir,
            timeout=30,
            capture_output=True
        )
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    # Gather outputs from result
    stdout = result.stdout
    stderr = result.stderr
    exit_code = result.returncode

    # Build result parts
    result_lines = []

    if stdout:  # If there is stdout, add it
        result_lines.append(f"STDOUT: \n{stdout}")
    if stderr:  # If there is stderr, add it
        result_lines.append(f"STDERR: \n{stderr}")
    if exit_code != 0:  # If the process failed, report it
        result_lines.append(f"Process exited with code {exit_code}")

    # If nothing at all was output
    if not result_lines:
        return "No output produced."  # No output produced

    # Return the combined result (hint: joinlines with '\n')
    return "\n".join(result_lines)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified python file with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)
