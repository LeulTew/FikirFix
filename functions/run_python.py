import os
import subprocess
import shlex


def run_python_file(working_directory, file_path, args=None):
    try:
        if args is None:
            args = []
        abs_working = os.path.abspath(working_directory)
        target = os.path.abspath(os.path.join(working_directory, file_path))

        if not (target == abs_working or target.startswith(abs_working + os.sep)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(target):
            return f'Error: File "{file_path}" not found.'

        if not target.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'

        cmd = ["python", target, *args]
        try:
            completed = subprocess.run(
                cmd,
                cwd=abs_working,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30,
                text=True,
            )
        except subprocess.TimeoutExpired:
            return "Error: executing Python file: timeout after 30 seconds"

        stdout = completed.stdout.strip()
        stderr = completed.stderr.strip()
        parts = ["STDOUT:", stdout] if stdout else []
        parts += ["STDERR:", stderr] if stderr else []
        if completed.returncode != 0:
            parts.append(f"Process exited with code {completed.returncode}")
        if not parts:
            return "No output produced."
        return "\n".join(parts)
    except Exception as e:
        return f"Error: executing Python file: {e}"
import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    if args is None:
        args = []

    try:
        abs_working = os.path.abspath(working_directory)
        target = os.path.abspath(os.path.join(working_directory, file_path))

        if not (target == abs_working or target.startswith(abs_working + os.sep)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(target):
            return f'Error: File "{file_path}" not found.'

        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'

        # Build command: use same python interpreter
        cmd = ["python", target] + list(args)

        try:
            completed = subprocess.run(
                cmd,
                cwd=working_directory,
                capture_output=True,
                text=True,
                timeout=30,
            )
        except Exception as e:
            return f"Error: executing Python file: {e}"

        stdout = completed.stdout or ""
        stderr = completed.stderr or ""

        parts = []
        if stdout:
            parts.append("STDOUT:\n" + stdout)
        if stderr:
            parts.append("STDERR:\n" + stderr)

        if completed.returncode != 0:
            parts.append(f"Process exited with code {completed.returncode}")

        if not parts:
            return "No output produced."

        return "\n".join(parts)
    except Exception as e:
        return f"Error: executing Python file: {e}"
import os
import sys
import subprocess


def run_python_file(working_directory, file_path, args=None):
    if args is None:
        args = []
    try:
        abs_working = os.path.abspath(working_directory)
        target = os.path.abspath(os.path.join(working_directory, file_path))

        if not (target == abs_working or target.startswith(abs_working + os.sep)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(target):
            return f'Error: File "{file_path}" not found.'

        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'

        cmd = [sys.executable, target] + list(args)

        try:
            completed = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30,
                cwd=working_directory,
            )
        except Exception as e:
            return f'Error: executing Python file: {e}'

        out = completed.stdout or ""
        err = completed.stderr or ""

        parts = []
        if out:
            parts.append("STDOUT:\n" + out.rstrip())
        else:
            parts.append("STDOUT:")

        if err:
            parts.append("STDERR:\n" + err.rstrip())
        else:
            parts.append("STDERR:")

        if completed.returncode != 0:
            parts.append(f"Process exited with code {completed.returncode}")

        result = "\n".join(parts).strip()
        if not result:
            return "No output produced."
        return result

    except Exception as e:
        return f"Error: executing Python file: {e}"
