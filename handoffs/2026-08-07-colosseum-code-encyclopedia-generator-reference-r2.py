#!/usr/bin/env python3
"""
Revision-2 delta wrapper for the Colosseum code-encyclopedia reference candidate.

This file intentionally loads the r1 candidate and replaces only:
1. bounded language-preamble recognition; and
2. the undocumented diagnostic wording.

That structure keeps Agent 0's test-reported r1 safety behavior mechanically
separate from the r2 grammar correction. For Colosseum adoption, Agent 0 may
either retain this wrapper plus r1 or inline the same delta into one script.

Status: authored preflight handoff artifact; not executed by Preflight Architect.
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

R1_NAME = "2026-08-07-colosseum-code-encyclopedia-generator-reference-r1.py"
R1_PATH = Path(__file__).with_name(R1_NAME)

CPP_SUFFIXES = {".c", ".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp", ".hxx"}
CPP_PRAGMA_ONCE = re.compile(r"^#\s*pragma\s+once\s*$")
CPP_INCLUDE = re.compile(r"^#\s*include\b")
CPP_IFNDEF = re.compile(r"^#\s*ifndef\s+([A-Za-z_][A-Za-z0-9_]*)\s*$")
CPP_DEFINE = re.compile(r"^#\s*define\s+([A-Za-z_][A-Za-z0-9_]*)\s*$")


def load_r1():
    spec = importlib.util.spec_from_file_location("colosseum_encyclopedia_r1", R1_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load r1 candidate: {R1_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


R1 = load_r1()


def skip_blanks(lines: list[str], index: int) -> int:
    while index < len(lines) and not lines[index].strip():
        index += 1
    return index


def skip_cpp_preamble(lines: list[str], index: int) -> int:
    """Skip only a contiguous, bounded C/C++ declaration preamble."""
    guard_skipped = False
    while True:
        index = skip_blanks(lines, index)
        if index >= len(lines):
            return index

        stripped = lines[index].strip()

        if CPP_PRAGMA_ONCE.fullmatch(stripped):
            index += 1
            continue

        if not guard_skipped:
            guard = CPP_IFNDEF.fullmatch(stripped)
            if guard:
                define_index = skip_blanks(lines, index + 1)
                if define_index < len(lines):
                    define = CPP_DEFINE.fullmatch(lines[define_index].strip())
                    if define and define.group(1) == guard.group(1):
                        guard_skipped = True
                        index = define_index + 1
                        continue
                # An incomplete or mismatched guard is a hard stop.
                return index

        if CPP_INCLUDE.match(stripped):
            index += 1
            continue

        return index


def skip_qml_preamble(lines: list[str], index: int) -> int:
    """Skip only a contiguous run of QML imports, QML pragmas, and blanks."""
    while True:
        index = skip_blanks(lines, index)
        if index >= len(lines):
            return index
        stripped = lines[index].strip()
        if stripped.startswith("import ") or stripped.startswith("pragma "):
            index += 1
            continue
        return index


def skip_js_preamble(lines: list[str], index: int) -> int:
    index = skip_blanks(lines, index)
    if index < len(lines) and lines[index].strip() == ".pragma library":
        index += 1
    return skip_blanks(lines, index)


def first_comment_index(rel: str, lines: list[str]) -> int:
    suffix = Path(rel).suffix.lower()
    index = skip_blanks(lines, 0)
    if suffix in CPP_SUFFIXES:
        return skip_cpp_preamble(lines, index)
    if suffix == ".qml":
        return skip_qml_preamble(lines, index)
    if suffix == ".js":
        return skip_js_preamble(lines, index)
    return index


def extract_comment(rel: str, data: bytes) -> str | None:
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise R1.EncyclopediaError(f"source is not UTF-8: {rel}") from exc

    lines = text.splitlines(keepends=True)
    index = first_comment_index(rel, lines)
    if index >= len(lines):
        return None

    first = lines[index].lstrip()

    if first.startswith("//"):
        start = index
        last_comment = index
        while index < len(lines):
            stripped = lines[index].lstrip()
            if stripped.startswith("//"):
                last_comment = index
                index += 1
                continue
            if not lines[index].strip():
                index += 1
                continue
            break
        return "".join(lines[start : last_comment + 1]).rstrip("\r\n")

    if first.startswith("/*"):
        start = index
        while index < len(lines):
            end = lines[index].find("*/")
            if end >= 0:
                return (
                    "".join(lines[start:index]) + lines[index][: end + 2]
                ).rstrip("\r\n")
            index += 1
        raise R1.EncyclopediaError(f"unterminated top block comment: {rel}")

    return None


R1.extract_comment = extract_comment

_r1_render = R1.render


def render(*args, **kwargs) -> str:
    return _r1_render(*args, **kwargs).replace(
        "_No top-of-file explanatory comment was harvested._",
        "_No explanatory comment was harvested after the allowed file preamble._",
    )


R1.render = render


if __name__ == "__main__":
    raise SystemExit(R1.main())
