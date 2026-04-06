import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    workdir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(workdir_abs, file_path))

    valid_target_dir = os.path.commonpath([target_dir, workdir_abs]) == workdir_abs
    if not valid_target_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_dir):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if not target_dir.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", target_dir]

    if args is not None:
        command.extend(args)

    output = []
    result = subprocess.run(
        command, text=True, timeout=30, capture_output=True, cwd=workdir_abs
    )

    if result.returncode != 0:
        output.append(f"Process exited with code {result.returncode}")

    if result.stdout == "" and result.stderr == "":
        output.append("No output produced")

    if result.stdout != "":
        output.append(f"STDOUT:\n{result.stdout}")

    if result.stderr != "":
        output.append(f"STDERR:\n{result.stderr}")

    return "\n".join(output)
