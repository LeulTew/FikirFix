import runpy
import sys
from typer.testing import CliRunner

from fikirfix import cli


def test_run_forwards_flags(monkeypatch):
    captured = {}

    def fake_run_path(path, run_name=None):
        # capture the sys.argv that the CLI set before invoking runpy
        captured['argv'] = list(sys.argv)

    monkeypatch.setattr(runpy, 'run_path', fake_run_path)

    runner = CliRunner()
    result = runner.invoke(cli.app, ['run', 'do something', '--dry-run', '--allow-writes', '--confirm'])
    # runpy.run_path was called and captured argv
    assert 'argv' in captured
    assert '--dry-run' in captured['argv']
    assert '--allow-writes' in captured['argv']
    assert '--confirm' in captured['argv']
    # CLI should exit cleanly (our fake run_path doesn't raise)
    assert result.exit_code == 0
