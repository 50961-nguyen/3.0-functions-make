import ast
import math
import pytest
from random import randint

from func_make import calculate_triangle, calculate_slope, main

def _source() -> str:
    with open("func_make.py", encoding="utf-8") as f:
        return f.read()

def _tree() -> ast.Module:
    return ast.parse(_source())

def _module_docstring() -> str:
    return ast.get_docstring(_tree()) or ""

def _func_node(func_name: str) -> ast.FunctionDef | None:
    for node in ast.walk(_tree()):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            return node
    return None

def _func_docstring(func_name: str) -> str:
    node = _func_node(func_name)
    return ast.get_docstring(node) or "" if node else ""

def _func_source(func_name: str) -> str:
    node = _func_node(func_name)
    return ast.get_source_segment(_source(), node) or "" if node else ""

def _annotation_str(annotation) -> str:
    """Convert an AST annotation node to a readable string."""
    if annotation is None:
        return ""
    return ast.unparse(annotation)

# ── header comment tests ──────────────────────────────────────────────────────

class TestHeaderComments:

    def test_header_exists(self):
        assert _module_docstring().strip(), (
            "Missing module-level header comment. Add a triple-quoted string at "
            "the top of func_make.py with author, date, and a short description."
        )

    def test_header_has_author(self):
        assert "author" in _module_docstring().lower(), (
            "Header comment is missing an 'author' line.  Example:  author: Your Name"
        )

    def test_header_has_date(self):
        assert "date" in _module_docstring().lower(), (
            "Header comment is missing a 'date' line.  Example:  date: April 2, 2026"
        )

    def test_header_has_description(self):
        lines = [
            ln.strip()
            for ln in _module_docstring().splitlines()
            if ln.strip() and not ln.lower().lstrip().startswith(("author", "date"))
        ]
        assert lines, (
            "Header comment should include a short description of the file, "
            "e.g. 'Functions Make'."
        )

# ── docstring tests ───────────────────────────────────────────────────────────

class TestDocstrings:

    @pytest.mark.parametrize("func_name", ["calculate_triangle", "calculate_slope"])
    def test_docstring_exists(self, func_name):
        assert _func_docstring(func_name).strip(), (
            f"'{func_name}' is missing a docstring. Add a triple-quoted string "
            "as the very first statement of the function."
        )

    def test_main_docstring_exists(self):
        assert _func_docstring("main").strip(), (
            "main() is missing a docstring. Add a triple-quoted string describing "
            "what main does as its very first statement."
        )

    @pytest.mark.parametrize("func_name", ["calculate_triangle", "calculate_slope"])
    def test_docstring_has_description(self, func_name):
        ds = _func_docstring(func_name)
        first_line = next((ln.strip() for ln in ds.splitlines() if ln.strip()), "")
        assert first_line and first_line.lower() not in ("args:", "returns:", "example:", "examples:"), (
            f"'{func_name}' docstring should start with a plain-English description "
            "of what the function does before listing Args/Returns/Example."
        )

    @pytest.mark.parametrize("func_name", ["calculate_triangle", "calculate_slope"])
    def test_docstring_has_args_section(self, func_name):
        ds = _func_docstring(func_name).lower()
        assert "args:" in ds or "arguments:" in ds or "parameters:" in ds, (
            f"'{func_name}' docstring is missing an 'Args:' section."
        )

    @pytest.mark.parametrize("func_name", ["calculate_triangle", "calculate_slope"])
    def test_docstring_has_returns_section(self, func_name):
        ds = _func_docstring(func_name).lower()
        assert "returns:" in ds or "return:" in ds, (
            f"'{func_name}' docstring is missing a 'Returns:' section."
        )

    @pytest.mark.parametrize("func_name", ["calculate_triangle", "calculate_slope"])
    def test_docstring_has_example_section(self, func_name):
        ds = _func_docstring(func_name).lower()
        assert "example" in ds, (
            f"'{func_name}' docstring is missing an 'Example' or 'Examples:' section."
        )

# ── type annotation tests ─────────────────────────────────────────────────────

class TestTypeAnnotations:

    def test_calculate_triangle_param_annotated(self):
        node = _func_node("calculate_triangle")
        assert node, "calculate_triangle function not found."
        unannotated = [
            arg.arg for arg in node.args.args if arg.annotation is None
        ]
        assert not unannotated, (
            f"calculate_triangle parameter(s) missing type annotations: {unannotated}. "
            "Example: def calculate_triangle(n: int)"
        )

    def test_calculate_triangle_param_type(self):
        node = _func_node("calculate_triangle")
        assert node, "calculate_triangle function not found."
        for arg in node.args.args:
            assert _annotation_str(arg.annotation) == "int", (
                f"Parameter '{arg.arg}' in calculate_triangle should be annotated as 'int', "
                f"got '{_annotation_str(arg.annotation)}'."
            )

    def test_calculate_triangle_return_annotated(self):
        node = _func_node("calculate_triangle")
        assert node, "calculate_triangle function not found."
        assert node.returns is not None, (
            "calculate_triangle is missing a return type annotation. "
            "Example: def calculate_triangle(n: int) -> int"
        )

    def test_calculate_triangle_return_type(self):
        node = _func_node("calculate_triangle")
        assert node and node.returns is not None, "calculate_triangle missing return annotation."
        ret = _annotation_str(node.returns)
        assert ret == "int", (
            f"calculate_triangle return type should be 'int', got '{ret}'."
        )

    def test_calculate_slope_params_annotated(self):
        node = _func_node("calculate_slope")
        assert node, "calculate_slope function not found."
        unannotated = [
            arg.arg for arg in node.args.args if arg.annotation is None
        ]
        assert not unannotated, (
            f"calculate_slope parameter(s) missing type annotations: {unannotated}. "
            "Example: def calculate_slope(x1: float, x2: float, y1: float, y2: float)"
        )

    def test_calculate_slope_params_type(self):
        node = _func_node("calculate_slope")
        assert node, "calculate_slope function not found."
        for arg in node.args.args:
            assert _annotation_str(arg.annotation) == "float", (
                f"Parameter '{arg.arg}' in calculate_slope should be annotated as 'float', "
                f"got '{_annotation_str(arg.annotation)}'."
            )

    def test_calculate_slope_return_annotated(self):
        node = _func_node("calculate_slope")
        assert node, "calculate_slope function not found."
        assert node.returns is not None, (
            "calculate_slope is missing a return type annotation. "
            "Example: def calculate_slope(...) -> float | str"
        )

    def test_calculate_slope_return_type(self):
        node = _func_node("calculate_slope")
        assert node and node.returns is not None, "calculate_slope missing return annotation."
        ret = _annotation_str(node.returns)
        # Accept both "float | str" and "str | float"
        assert ret in ("float | str", "str | float"), (
            f"calculate_slope return type should be 'float | str', got '{ret}'."
        )

# ── IPO comment tests ─────────────────────────────────────────────────────────

class TestIPOComments:

    def test_ipo_input_comment(self):
        src = _func_source("main").lower()
        assert "# input" in src, (
            "main() is missing an '# Input' comment. "
            "Mark where you receive/assign input values with '# Input'."
        )

    def test_ipo_processing_comment(self):
        src = _func_source("main").lower()
        assert "# processing" in src, (
            "main() is missing a '# Processing' comment. "
            "Mark where computation happens with '# Processing' or '# Processing/Output'."
        )

    def test_ipo_output_comment(self):
        src = _func_source("main").lower()
        # Accept "# output", "# processing/output", or "# processing / output"
        has_output = (
            "# output" in src
            or "processing/output" in src
            or "processing / output" in src
        )
        assert has_output, (
            "main() is missing an '# Output' comment. "
            "Mark where results are printed with '# Output' or combine as '# Processing/Output'."
        )

# ── functionality tests ───────────────────────────────────────────────────────

def test_calc_triangle():
    num = randint(5, 100)
    expected = sum(range(1, num + 1))
    assert calculate_triangle(num) == expected

def test_calc_triangle_small():
    assert calculate_triangle(6) == 21

def test_calc_slope_normal():
    assert calculate_slope(1, 2, 1, 2) == 1.0

def test_calc_slope_undefined():
    result = calculate_slope(3, 3, 1, 5)
    assert result == "undefined", (
        f"calculate_slope should return the string 'undefined' when x1 == x2, got {result!r}"
    )

def test_calc_slope_negative():
    assert calculate_slope(0, 2, 4, 0) == -2.0

def test_calc_slope_returns_float_when_defined():
    result = calculate_slope(0, 4, 0, 8)
    assert isinstance(result, float), (
        f"calculate_slope should return a float when slope is defined, got {type(result).__name__}"
    )