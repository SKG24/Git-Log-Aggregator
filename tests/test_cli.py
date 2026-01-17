import subprocess
import sys

def run_cli(*args):
    # Run `python -m aggregator ...`
    return subprocess.run([sys.executable, "-m", "aggregator", *args],
                          capture_output=True, text=True)

def test_cli_version():
    out = run_cli("--version")
    assert out.returncode == 0
    assert "git-log-aggregator" in out.stdout

def test_cli_help():
    out = run_cli()
    assert out.returncode == 0
    assert "usage" in out.stdout.lower()
