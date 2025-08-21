import os
import sys
from pathlib import Path
import runpy
import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
import traceback

from fikirfix import __version__

app = typer.Typer(help="FikirFix — Agentic development helpers")
console = Console()


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


@app.callback(invoke_without_command=True)
def root(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        console.print(Panel(Text("FikirFix — run `fikirfix --help` for commands", justify="center"), subtitle=f"v{__version__}"))


@app.command()
def run(
    prompt: str = typer.Argument(..., help="Prompt for the agent"),
    verbose: bool = typer.Option(False, "--verbose", help="Show verbose output"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would change without applying writes"),
    allow_writes: bool = typer.Option(False, "--allow-writes", help="Allow write operations (opt-in)"),
    confirm: bool = typer.Option(False, "--confirm", help="Confirm that you want to apply writes when allowed"),
):
    """Run the LLM-backed agent with a prompt.

    Example: fikirfix run "fix the bug: 3 + 7 * 2 shouldn't be 20"
    """
    project_root = _project_root()
    main_path = project_root / "main.py"
    if not main_path.exists():
        console.print("[bold red]Error:[/bold red] main.py not found in project root")
        raise typer.Exit(code=2)

    console.rule("Running agent")
    console.print(f"[bold]Prompt[/bold]: {prompt}")
    sys.argv = [str(main_path), prompt]
    if verbose:
        sys.argv.append("--verbose")
    if dry_run:
        sys.argv.append("--dry-run")
    if allow_writes:
        sys.argv.append("--allow-writes")
    if confirm:
        sys.argv.append("--confirm")
    try:
        runpy.run_path(str(main_path), run_name="__main__")
    except Exception as exc:
        console.print(f"[red]Agent execution failed:[/red] {exc}")
        raise typer.Exit(code=3)


@app.command()
def calc(expression: str = typer.Argument(..., help="Expression to evaluate, e.g. '3 + 7 * 2'")):
    """Evaluate an expression using the bundled `calculator` example."""
    project_root = _project_root()
    calc_main = project_root / "calculator" / "main.py"
    if not calc_main.exists():
        console.print("[bold red]Error:[/bold red] calculator/main.py not found")
        raise typer.Exit(code=2)
    console.rule("Calculator")
    sys.argv = [str(calc_main), expression]
    # Run from the calculator directory so imports like `from pkg...` resolve
    prev_cwd = os.getcwd()
    prev_sys_path = list(sys.path)
    try:
        # Ensure imports like `from pkg...` resolve when running via runpy
        sys.path.insert(0, str(calc_main.parent))
        os.chdir(str(calc_main.parent))
        runpy.run_path(str(calc_main), run_name="__main__")
    except Exception as exc:
        console.print(f"[red]Execution failed:[/red] {exc}")
        # Print full traceback to aid test debugging
        import traceback as _tb

        _tb.print_exc()
        raise typer.Exit(code=3)
    finally:
        # attempt to restore previous working directory first
        try:
            os.chdir(prev_cwd)
        except Exception:
            pass
        # always restore sys.path to its previous state
        try:
            sys.path[:] = prev_sys_path
        except Exception:
            pass


@app.command()
def inspect(path: str = typer.Argument(".", help="Path to list files from (relative to repo root)")):
    """Quick helper to print a directory listing for local inspection."""
    project_root = _project_root()
    target = project_root / path
    if not target.exists():
        console.print(f"[bold red]Path not found:[/bold red] {path}")
        raise typer.Exit(code=1)

    table = Table(title=f"Listing: {path}")
    table.add_column("Name")
    table.add_column("Type")
    table.add_column("Size", justify="right")
    for p in sorted(target.iterdir()):
        typ = "dir" if p.is_dir() else "file"
        size = "-" if p.is_dir() else str(p.stat().st_size)
        table.add_row(p.name, typ, size)
    console.print(table)


@app.command()
def version():
    """Show package version."""
    console.print(f"FikirFix v{__version__}")


@app.command()
def doctor():
    """Run quick environment checks to ensure the CLI will work for you."""
    project_root = _project_root()
    table = Table(title="Environment check")
    table.add_column("Check")
    table.add_column("Result")

    # Python version
    table.add_row("Python", sys.version.splitlines()[0])

    # Gemin API key
    gem_key = os.environ.get("GEMINI_API_KEY")
    table.add_row("GEMINI_API_KEY", "set" if gem_key else "NOT SET")

    # main.py presence
    table.add_row("main.py present", "yes" if (project_root / "main.py").exists() else "no")

    console.print(table)


def main():
    app()
