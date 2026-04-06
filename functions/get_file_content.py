import os
from google.genai import types

MAX_CHARS = 10000

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file relative to the working directory. Returns up to 10000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)


def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            MAX_CHARS = 10000
            content = f.read(MAX_CHARS)

            if f.read(1):
                content += (
                    f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

            return content

    except Exception as e:
        return f"Error: {e}"


def get_file_content(working_directory, file_path):
    try:
        workdir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(workdir_abs, file_path))

        valid_target_dir = os.path.commonpath([target_dir, workdir_abs]) == workdir_abs
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        return read_file(target_dir)

    except Exception as e:
        return f"Error: {e}"
