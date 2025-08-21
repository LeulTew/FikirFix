import sys
from types import ModuleType, SimpleNamespace


def pytest_configure(config):
    # Provide a minimal fake google.genai module so importing main.py works during tests
    if "google.genai" not in sys.modules:
        mod_google = ModuleType("google")
        mod_genai = ModuleType("google.genai")

        # Build a robust types namespace with minimal API surface used by the codebase
        types_ns = SimpleNamespace()

        # Schema / FunctionDeclaration / Tool placeholders used at import time
        types_ns.Tool = lambda *a, **k: None
        types_ns.FunctionDeclaration = lambda *a, **k: None
        types_ns.Schema = lambda *a, **k: None
        types_ns.GenerateContentConfig = lambda *a, **k: None
        types_ns.Type = SimpleNamespace(OBJECT="object", STRING="string", ARRAY="array")

        # Minimal Part/Content placeholders matching expectations in main.py
        class Part:
            def __init__(self, text=None):
                self.text = text
                self.function_response = None

            @staticmethod
            def from_function_response(name, response):
                p = SimpleNamespace()
                p.function_response = SimpleNamespace(response=response)
                return p

        class Content:
            def __init__(self, role=None, parts=None, text=None):
                self.role = role
                self.parts = parts or []
                self.text = text

        types_ns.Part = Part
        types_ns.Content = Content

        mod_genai.types = types_ns
        mod_genai.Client = lambda api_key=None: None

        # Also set attribute on the top-level google module for completeness
        mod_google.genai = mod_genai

        sys.modules["google"] = mod_google
        sys.modules["google.genai"] = mod_genai
