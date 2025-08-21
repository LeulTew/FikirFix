import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    try:
        # Resolve absolute paths
        abs_working = os.path.abspath(working_directory)
        target = os.path.abspath(os.path.join(working_directory, directory))

        # Ensure target is within the working directory
        # Allow target == abs_working or target under it
        if not (target == abs_working or target.startswith(abs_working + os.sep)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check directory exists and is a directory
        if not os.path.isdir(target):
            return f'Error: "{directory}" is not a directory'

        entries = sorted(os.listdir(target))
        lines = []
        for name in entries:
            path = os.path.join(target, name)
            try:
                size = os.path.getsize(path)
            except OSError as e:
                return f"Error: {e}"
            is_dir = os.path.isdir(path)
            lines.append(f" - {name}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


def get_file_content(working_directory, file_path):
    try:
        abs_working = os.path.abspath(working_directory)
        target = os.path.abspath(os.path.join(working_directory, file_path))

        if not (target == abs_working or target.startswith(abs_working + os.sep)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Lazy import config to avoid circular imports elsewhere
        from functions.config import MAX_CHARS

        with open(target, "r", errors="replace") as f:
            content = f.read(MAX_CHARS)

        # If file longer than MAX_CHARS, append truncation message
        try:
            full_size = os.path.getsize(target)
        except OSError:
            full_size = None

        if full_size is not None and full_size > MAX_CHARS:
            content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content
    except Exception as e:
        return f"Error: {e}"


def write_file(working_directory, file_path, content):
    try:
        abs_working = os.path.abspath(working_directory)
        target = os.path.abspath(os.path.join(working_directory, file_path))

        if not (target == abs_working or target.startswith(abs_working + os.sep)):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Ensure directory exists
        parent = os.path.dirname(target)
        if parent and not os.path.exists(parent):
            os.makedirs(parent, exist_ok=True)

        with open(target, "w", encoding="utf-8", errors="replace") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"


# Function schema for LLM tool declaration (only get_files_info for now)
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description=(
                    "The directory to list files from, relative to the working directory. "
                    "If not provided, lists files in the working directory itself."
                ),
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a text file (truncated) within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the file to read.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes (overwrites) a file with provided content within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the file to write.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write into the file.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional string arguments inside the working directory and returns its output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the Python file to run.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of string arguments passed to the script.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)


