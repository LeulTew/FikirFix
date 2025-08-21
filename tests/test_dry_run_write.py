import sys
import types as _types


# Inject a minimal fake google.genai.types module so tests don't require the real package
fake_types_mod = _types.SimpleNamespace()


class Part:
    def __init__(self):
        self.function_response = None

    @staticmethod
    def from_function_response(name, response):
        p = Part()
        p.function_response = _types.SimpleNamespace(response=response)
        return p


class Content:
    def __init__(self, role=None, parts=None):
        self.role = role
        self.parts = parts or []


fake_types_mod.Part = Part
fake_types_mod.Content = Content

# Minimal placeholders required by functions/get_files_info import-time
fake_types_mod.FunctionDeclaration = lambda *a, **k: None
fake_types_mod.Schema = lambda *a, **k: None
fake_types_mod.Type = _types.SimpleNamespace(OBJECT="object", STRING="string", ARRAY="array")
fake_types_mod.Tool = lambda *a, **k: None
fake_types_mod.GenerateContentConfig = lambda *a, **k: None

fake_genai = _types.SimpleNamespace(types=fake_types_mod, Client=lambda api_key=None: None)

mod_google = _types.ModuleType("google")
mod_genai = _types.ModuleType("google.genai")
mod_genai.types = fake_types_mod
mod_genai.Client = lambda api_key=None: None
sys.modules["google"] = mod_google
sys.modules["google.genai"] = mod_genai

import importlib.util
from pathlib import Path

# Import main.py as a module regardless of environment
spec = importlib.util.spec_from_file_location("main", str(Path(__file__).resolve().parents[1] / "main.py"))
main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main)
call_function = main.call_function


class FakeFunctionCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args


def test_dry_run_write_diff(tmp_path, monkeypatch):
    # Prepare a target file inside calculator/ for the test
    calc_dir = tmp_path / "calculator"
    calc_dir.mkdir()
    target = calc_dir / "sample.txt"
    # existing content
    target.write_text("line1\nline2\n")

    # Run from the tmp_path so main.py's relative calculator path resolves to this directory
    monkeypatch.chdir(str(tmp_path))

    # Fake function call: write_file with content that changes one line
    args = {"file_path": "sample.txt", "content": "line1\nmodified_line2\n"}
    fc = FakeFunctionCall("write_file", args)

    # Call with dry_run=True — should return a unified diff and not modify the file
    content = call_function(fc, verbose=False, allow_writes=False, confirm=False, dry_run=True)

    # Extract response
    prt = content.parts[0]
    resp = getattr(prt, "function_response").response
    text = resp.get("result") if isinstance(resp, dict) else resp
    assert "DRY-RUN unified diff" in text
    assert ("-line2" in text) or ("- line2" in text)
    assert ("+modified_line2" in text) or ("+ modified_line2" in text)

    # Ensure file was not modified
    assert target.read_text() == "line1\nline2\n"
