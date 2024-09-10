"""
Test the source code provided by the documentation.

See
- doctest documentation: https://docs.python.org/3/library/doctest.html

"""

import doctest
import importlib
import pathlib
import sys

import pytest

HERE = pathlib.Path(__file__).parent
PROJECT_PATH = HERE.parent
LIB_PATH = PROJECT_PATH / "src" / "mergecal"

MODULE_NAMES = [name for name in sys.modules.keys() if name.startswith("mergecal")]


@pytest.mark.parametrize("module_name", MODULE_NAMES)
def test_docstring_of_python_file(module_name):
    """Runs doctest on the Python module."""
    module = importlib.import_module(module_name)
    test_result = doctest.testmod(module, name=module_name)
    assert test_result.failed == 0, f"{test_result.failed} errors in {module_name}"


# This collection needs to exclude .tox and other subdirectories
DOCUMENT_PATHS = [
    str(name.relative_to(PROJECT_PATH)) for name in PROJECT_PATH.rglob("*.md")
]


@pytest.mark.parametrize("document", DOCUMENT_PATHS)
def test_documentation_file(document, env_for_doctest):
    """
    Run doctest on a documentation file.

    functions are also replaced to work.
    """
    test_result = doctest.testfile(
        PROJECT_PATH / document,
        module_relative=False,
        globs=env_for_doctest,
        raise_on_error=False,
    )
    assert test_result.failed == 0, f"{test_result.failed} errors in {document.name}"
