"""
Multiple string utils collection.
"""
import builtins
import keyword
import textwrap
import typing
from typing import Dict, List
from unittest.mock import MagicMock

from botocore.utils import get_service_module_name

RESERVED_NAMES = set(
    (
        *dir(typing),
        *dir(builtins),
        *keyword.kwlist,
    )
)
MAX_DOCSTRING_LENGTH: int = 300


def get_class_prefix(func_name: str) -> str:
    """
    Get a valid Python class prefix from `func_name`.

    Arguments:
        func_name -- Any string.

    Returns:
        String with a class prefix.
    """
    parts = [f"{i[:1].upper()}{i[1:]}" for i in func_name.split("_") if i]
    return "".join(parts)


def get_line_with_indented(input_string: str, multi_first_line: bool = False) -> str:
    """
    Get first line of the string with all indented lines.

    Fixes invalid unindent.

    Arguments:
        input_string -- Input string.

    Returns:
        A string with first line and following indented lines.
    """
    result: List[str] = []
    indent_stack: List[int] = []
    for line in input_string.splitlines():
        line_indent = len(line) - len(line.lstrip())
        if not indent_stack:
            indent_stack.append(line_indent)
            result.append(line)
            continue

        if not line:
            result.append(line)
            continue

        if line_indent < indent_stack[0]:
            break

        if line_indent == indent_stack[0]:
            if not multi_first_line:
                break

            if len(indent_stack) > 1:
                break

        if line_indent == indent_stack[-1]:
            result.append(line)
            continue

        if line_indent > indent_stack[-1]:
            indent_stack.append(line_indent)
            result.append(line)
            continue

        while len(indent_stack) > 1 and line_indent <= indent_stack[-2]:
            indent_stack.pop()

        if indent_stack[-1] != line_indent:
            result.append(f"{' ' * indent_stack[-1]}{line[line_indent:]}")
            continue

        result.append(line)

    while result and not result[-1]:
        result.pop()

    return "\n".join(result)


def get_anchor_link(text: str) -> str:
    """
    Convert header to markdown anchor link.
    """
    return text.strip().replace(" ", "-").replace(".", "").lower()


def is_reserved(word: str) -> bool:
    """
    Check whether varialbe name conflicts with Python reserved names.
    """
    return word in RESERVED_NAMES


def get_short_docstring(doc: str) -> str:
    """
    Create a short docstring from boto3 documentation.

    Trims docstring to 300 chars.
    Removes double and trible backticks.
    Ensures that backticks are closed.
    Wraps docstring to 80 chars.
    """
    doc = str(doc)
    if len(doc) > MAX_DOCSTRING_LENGTH:
        doc = f"{doc[:MAX_DOCSTRING_LENGTH - 3]}..."
    result = []
    if not doc:
        return ""
    for line in doc.splitlines():
        line = line.strip().rstrip("::")
        if line.startswith(":"):
            break
        if not line:
            continue
        if ". " in line:
            result.append(line.split(". ")[0])
            break
        result.append(line)
        if line.endswith("."):
            break

    result_str = " ".join(result).replace("```", "`").replace("``", "`").strip()
    if result_str.count("`") % 2:
        result_str = f"{result_str}`"
    if result_str and not result_str.endswith("."):
        result_str = f"{result_str}."

    return "\n".join(textwrap.wrap(result_str, width=80))


def get_botocore_class_name(metadata: Dict[str, str]) -> str:
    """
    Get Botocore class name from Service metadata.
    """
    service_model = MagicMock()
    service_model.service_name = metadata.get("serviceId", "")
    service_model.metadata = metadata
    return get_service_module_name(service_model)


def get_min_build_version(version: str) -> str:
    """
    Get min version 5 micro releases lower that `version`.

    Minimum micro is 0.
    """
    major = minor = micro = "0"
    if version.count(".") > 2:
        major, minor, micro, _ = version.split(".", 3)
    else:
        major, minor, micro = version.split(".", 2)
    new_micro = max(int(micro) - 5, 0)
    return f"{major}.{minor}.{new_micro}"
