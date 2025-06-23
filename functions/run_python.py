import os
import subprocess

def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target = os.path.abspath(os.path.join(working_directory, file_path))
    if os.path.commonpath([abs_working_dir, target]) != abs_working_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory.'
    if not os.path.isfile(target):
        return f'Error: File "{file_path}" not found.'
    if not target.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(
            ["python3", target],
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