import os


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
