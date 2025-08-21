import os
from functions.get_files_info import get_files_info, get_file_content


def test_get_files_info_list_calculator_root():
    res = get_files_info("calculator", ".")
    assert isinstance(res, str)
    assert "pkg" in res or "main.py" in res


def test_get_file_content_render():
    content = get_file_content("calculator", "pkg/render.py")
    assert isinstance(content, str)
    assert "def render" in content or "render(" in content
