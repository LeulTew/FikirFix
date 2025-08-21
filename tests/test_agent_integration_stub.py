import sys
from types import SimpleNamespace


class Part:
    def __init__(self, text=None):
        self.text = text
        self.function_response = None

    @staticmethod
    def from_function_response(name, response):
        p = Part()
        p.function_response = SimpleNamespace(response=response)
        return p


class Content:
    def __init__(self, role=None, parts=None, text=None):
        self.role = role
        self.parts = parts or []
        self.text = text


def test_agent_loop_with_stub(monkeypatch, capsys):
    # Inject minimal fake google.genai.types before importing main
    from types import ModuleType

    # Build a robust fake types namespace with required placeholders
    types_ns = SimpleNamespace()
    types_ns.Tool = lambda *a, **k: None
    types_ns.FunctionDeclaration = lambda *a, **k: None
    types_ns.Schema = lambda *a, **k: None
    types_ns.GenerateContentConfig = lambda *a, **k: None
    types_ns.Type = SimpleNamespace(OBJECT="object", STRING="string", ARRAY="array")
    types_ns.Part = Part
    types_ns.Content = Content

    mod_google = ModuleType("google")
    mod_genai = ModuleType("google.genai")
    mod_genai.types = types_ns
    mod_genai.Client = lambda api_key=None: None

    # Make `from google import genai` work by attaching genai to the google module
    mod_google.genai = mod_genai

    sys.modules["google"] = mod_google
    sys.modules["google.genai"] = mod_genai

    import importlib
    importlib.reload(sys.modules.get("main")) if "main" in sys.modules else None

    import importlib.util
    from pathlib import Path

    # Import main.py as a module regardless of environment
    spec = importlib.util.spec_from_file_location(
        "main",
        str(Path(__file__).resolve().parents[1] / "main.py"),
    )
    main = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main)
    run_main = main.main

    # Provide fake types expected by main (Part.from_function_response, Content)
    fake_types = SimpleNamespace(Part=Part, Content=Content)
    # Minimal placeholders to satisfy import-time expectations in functions/
    fake_types.FunctionDeclaration = lambda *a, **k: None
    fake_types.Schema = lambda *a, **k: None
    fake_types.Type = SimpleNamespace(OBJECT="object", STRING="string", ARRAY="array")
    fake_types.Tool = lambda *a, **k: None
    # Minimal GenerateContentConfig placeholder used by main.main
    fake_types.GenerateContentConfig = lambda *a, **k: None
    monkeypatch.setattr(main, "types", fake_types)

    # Prepare stubbed model responses: first ask for get_files_info, then final text
    resp1 = SimpleNamespace(candidates=[SimpleNamespace(content=SimpleNamespace(parts=[SimpleNamespace(function_call=SimpleNamespace(name="get_files_info", args={"directory": "."}))]))])
    resp2 = SimpleNamespace(candidates=[], text="Agent final answer: inspected files")
    responses = [resp1, resp2]

    def generate_content_stub(*args, **kwargs):
        return responses.pop(0)

    stub_models = SimpleNamespace(generate_content=generate_content_stub)
    monkeypatch.setattr(main, "CLIENT", SimpleNamespace(models=stub_models))

    # Run from repo root so calculator exists
    monkeypatch.chdir(".")

    # Provide argv for main
    monkeypatch.setattr(sys, "argv", ["main.py", "inspect calculator"])

    # Run main — should execute the stubbed loop without raising
    run_main()

    captured = capsys.readouterr()
    assert " - Calling function: get_files_info" in captured.out
    assert "Final response:" in captured.out
    assert "Agent final answer: inspected files" in captured.out
