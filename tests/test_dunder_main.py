import subprocess
import sys


def test_can_run_as_python_module():
    """Run the CLI as a Python module."""
    result = subprocess.run(  # noqa: S603
        [sys.executable, "-m", "mergecal", "--help"],
        check=True,
        capture_output=True,
    )
    assert result.returncode == 0
    assert b"mergecal [OPTIONS]" in result.stdout
