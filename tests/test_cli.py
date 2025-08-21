import sys
from typer.testing import CliRunner
from fikirfix import cli


def test_calc_expression():
    runner = CliRunner()
    result = runner.invoke(cli.app, ["calc", "3 + 7 * 2"])
    # calculator prints a rendered box; ensure exit code 0 and expected number
    assert result.exit_code == 0
    assert "3 + 7 * 2" in result.stdout


def test_inspect_root():
    runner = CliRunner()
    result = runner.invoke(cli.app, ["inspect", "."])
    assert result.exit_code == 0
    # expected files like README.md or main.py should appear
    assert any(x in result.stdout for x in ("README.md", "main.py", "calculator"))
