#!/usr/bin/env python3
"""Error-handling lint — docs/technical/ERROR_HANDLING.md (no silent exceptions)."""
from __future__ import annotations

import ast
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
GAME_GD_DIRS = (ROOT / "game" / "scripts", ROOT / "game" / "tests")
MCP_TS_DIR = ROOT / "tools" / "godot-mcp-pro-server"

BASH_FORBIDDEN_RE = re.compile(r"&&\s+.+\s+\|\|\s+fail\b|&&\s+ok\b.+\|\|\s+fail\b")
BASH_SWALLOW_TRUE_RE = re.compile(r"\|\|\s*true\b")
BASH_SWALLOW_STDERR_RE = re.compile(r"2>/dev/null")
BASH_SWALLOW_OK_LINE_RE = re.compile(r"#\s*swallow-ok\b")
BASH_SWALLOW_OK_SCRIPT_PREFIXES = (
    "install_",
    "ensure_",
    "setup_",
    "run_post_",
    "run_alignment_",
    "run_visual_",
    "run_model_",
    "run_audio_",
    "rebuild_",
    "qa_emit_",
)
BASH_SWALLOW_OK_INLINE_RE = re.compile(
    r"merge-base|rev-list|echo unknown|head -1|print -quit|is_file\(\)|--if-present"
)

GD_EMPTY_PUSH_ERROR_RE = re.compile(r'push_error\s*\(\s*["\'][\s]*["\']\s*\)')
GD_BARE_PUSH_ERROR_RE = re.compile(r"push_error\s*\(\s*\)")
GD_RES_PATH_IN_PRINT_RE = re.compile(r'print\s*\([^)]*res://')

TS_SILENT_CATCH_RE = re.compile(
    r"catch\s*(?:\([^)]*\))?\s*\{([^}]*)\}",
    re.MULTILINE | re.DOTALL,
)
TS_AUDIBLE_CATCH_RE = re.compile(
    r"console\.(error|warn)|throw\s|return\s+\{[^}]*error",
)


def _exc_type_name(handler: ast.ExceptHandler) -> str:
    if handler.type is None:
        return "bare except"
    return ast.unparse(handler.type)


def _is_print_call(node: ast.AST) -> bool:
    return isinstance(node, ast.Call) and (
        (isinstance(node.func, ast.Name) and node.func.id == "print")
        or (isinstance(node.func, ast.Attribute) and node.func.attr == "print")
    )


def _is_logging_call(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
        return False
    if isinstance(node.func.value, ast.Name) and node.func.value.id == "logging":
        return node.func.attr in {"debug", "info", "warning", "error", "exception", "critical"}
    return False


def _is_errors_append(stmt: ast.stmt) -> bool:
    if not isinstance(stmt, ast.Expr) or not isinstance(stmt.value, ast.Call):
        return False
    call = stmt.value
    if not isinstance(call.func, ast.Attribute) or call.func.attr != "append":
        return False
    return isinstance(call.func.value, ast.Name) and call.func.value.id == "errors"


def _is_cast_fallback_handler(handler: ast.ExceptHandler) -> bool:
    """`try: x = int(v) except ValueError: x = v` — control flow, not swallowing."""
    if not isinstance(handler.type, ast.Name) or handler.type.id != "ValueError":
        return False
    if len(handler.body) != 1:
        return False
    return isinstance(handler.body[0], ast.Assign)


def _return_propagates_error(node: ast.Return) -> bool:
    if node.value is None:
        return False
    if isinstance(node.value, ast.Tuple) and len(node.value.elts) >= 2:
        return True
    if isinstance(node.value, ast.List) and node.value.elts:
        return True
    return False


def _assign_records_error(stmt: ast.stmt) -> bool:
    if not isinstance(stmt, ast.Assign) or not isinstance(stmt.value, ast.Dict):
        return False
    for key in stmt.value.keys:
        if isinstance(key, ast.Constant) and key.value == "error":
            return True
    return False


def _assign_from_caught_exc(stmt: ast.stmt, handler: ast.ExceptHandler) -> bool:
    if handler.name is None or not isinstance(stmt, ast.Assign):
        return False
    val = stmt.value
    return isinstance(val, ast.Name) and val.id == handler.name


def _stmt_is_audible(stmt: ast.stmt, handler: ast.ExceptHandler | None = None) -> bool:
    if isinstance(stmt, ast.Raise):
        return True
    if isinstance(stmt, ast.Return) and _return_propagates_error(stmt):
        return True
    if isinstance(stmt, ast.Expr):
        val = stmt.value
        if _is_print_call(val) or _is_logging_call(val):
            return True
        if isinstance(val, ast.Call) and isinstance(val.func, ast.Attribute):
            if val.func.attr in {"append", "extend"}:
                return True
    if _is_errors_append(stmt):
        return True
    if handler is not None and _assign_from_caught_exc(stmt, handler):
        return True
    if _assign_records_error(stmt):
        return True
    if isinstance(stmt, ast.Try):
        return any(_handler_is_audible(h) for h in stmt.handlers)
    return False


def _is_valueerror_return_fallback(handler: ast.ExceptHandler) -> bool:
    """`except ValueError: return os.path.relpath(...)` — alternate path, not swallowing."""
    if not isinstance(handler.type, ast.Name) or handler.type.id != "ValueError":
        return False
    if len(handler.body) != 1 or not isinstance(handler.body[0], ast.Return):
        return False
    return handler.body[0].value is not None


def _handler_is_audible(handler: ast.ExceptHandler) -> bool:
    if _is_cast_fallback_handler(handler) or _is_valueerror_return_fallback(handler):
        return True
    body = handler.body
    if not body:
        return False
    if all(isinstance(stmt, ast.Pass) for stmt in body):
        return False
    return any(_stmt_is_audible(stmt, handler) for stmt in body)


def _is_optional_import_handler(handler: ast.ExceptHandler, module_level: bool) -> bool:
    if not module_level or handler.type is None:
        return False
    name = _exc_type_name(handler)
    if name not in {"ImportError", "ModuleNotFoundError"}:
        return False
    return all(isinstance(stmt, ast.Assign) for stmt in handler.body)


class SilentExceptVisitor(ast.NodeVisitor):
    def __init__(self, rel: str, errors: list[str]) -> None:
        self.rel = rel
        self.errors = errors
        self._depth = 0

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._depth += 1
        self.generic_visit(node)
        self._depth -= 1

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._depth += 1
        self.generic_visit(node)
        self._depth -= 1

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        module_level = self._depth == 0
        if _is_optional_import_handler(node, module_level):
            return
        if not _handler_is_audible(node):
            self.errors.append(
                f"{self.rel}:{node.lineno}: silent {_exc_type_name(node)} — "
                "log to stderr, raise, or errors.append (never swallow)"
            )
        self.generic_visit(node)


class FailPrintVisitor(ast.NodeVisitor):
    """[FAIL] lines must go to stderr — ERROR_HANDLING.md §2.1."""

    def __init__(self, rel: str, errors: list[str]) -> None:
        self.rel = rel
        self.errors = errors

    def visit_Call(self, node: ast.Call) -> None:
        if _is_print_call(node) and node.args:
            first = node.args[0]
            if isinstance(first, ast.Constant) and isinstance(first.value, str):
                if "[FAIL]" in first.value:
                    uses_stderr = any(
                        kw.arg == "file"
                        and isinstance(kw.value, ast.Attribute)
                        and kw.value.attr == "stderr"
                        for kw in node.keywords
                    )
                    if not uses_stderr:
                        self.errors.append(
                            f"{self.rel}:{node.lineno}: [FAIL] must use print(..., file=sys.stderr)"
                        )
        self.generic_visit(node)


def run_ruff_error_rules() -> list[str]:
    proc = subprocess.run(
        ["ruff", "check", str(TOOLS), "--select", "E722,S110,S112"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        return []
    return [line for line in proc.stdout.splitlines() if line.strip()]


def check_python_files(errors: list[str]) -> None:
    for path in sorted(TOOLS.rglob("*.py")):
        if path.name == "check_error_handling.py":
            continue
        rel = path.relative_to(ROOT).as_posix()
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=rel)
        except SyntaxError as exc:
            errors.append(f"{rel}:{exc.lineno}: syntax error — {exc.msg}")
            continue
        SilentExceptVisitor(rel, errors).visit(tree)
        FailPrintVisitor(rel, errors).visit(tree)


def _bash_swallow_allowed(script_name: str, line: str) -> bool:
    if BASH_SWALLOW_OK_LINE_RE.search(line):
        return True
    if any(script_name.startswith(prefix) for prefix in BASH_SWALLOW_OK_SCRIPT_PREFIXES):
        return True
    return bool(BASH_SWALLOW_OK_INLINE_RE.search(line))


def check_bash_scripts(errors: list[str]) -> None:
    for path in sorted(TOOLS.glob("*.sh")):
        rel = path.relative_to(ROOT).as_posix()
        raw = path.read_text(encoding="utf-8")
        head = "\n".join(raw.splitlines()[:20])
        if path.name.startswith(("check_", "run_")) and "set -euo pipefail" not in head:
            errors.append(f"{rel}: gate/run script must set -euo pipefail in first 20 lines")
        for line_no, line in enumerate(raw.splitlines(), 1):
            if BASH_FORBIDDEN_RE.search(line):
                errors.append(
                    f"{rel}:{line_no}: use if/else instead of && … || fail (ERROR_HANDLING.md §3.2)"
                )
            if not path.name.startswith(("check_", "validate_")):
                continue
            if _bash_swallow_allowed(path.name, line):
                continue
            if BASH_SWALLOW_TRUE_RE.search(line):
                errors.append(
                    f"{rel}:{line_no}: avoid `|| true` in gate scripts — use explicit if or "
                    "# swallow-ok (ERROR_HANDLING.md §3.2)"
                )
            if BASH_SWALLOW_STDERR_RE.search(line) and "||" in line:
                errors.append(
                    f"{rel}:{line_no}: avoid suppressing stderr with 2>/dev/null on failure paths — "
                    "use explicit if or # swallow-ok"
                )


def check_gdscript_files(errors: list[str]) -> int:
    checked = 0
    for base in GAME_GD_DIRS:
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.gd")):
            rel = path.relative_to(ROOT).as_posix()
            raw = path.read_text(encoding="utf-8")
            checked += 1
            if GD_EMPTY_PUSH_ERROR_RE.search(raw) or GD_BARE_PUSH_ERROR_RE.search(raw):
                errors.append(f"{rel}: push_error requires a non-empty actionable message")
            if GD_RES_PATH_IN_PRINT_RE.search(raw):
                errors.append(f"{rel}: do not print res:// paths — player-facing leak risk")
            for match in re.finditer(r"push_error\s*\([^)]+\)", raw):
                start = match.end()
                window = raw[start : start + 240]
                lines = [
                    ln.strip()
                    for ln in window.splitlines()[:6]
                    if ln.strip() and not ln.strip().startswith("#")
                ]
                if not lines:
                    continue
                first = lines[0]
                if first.startswith(("return", "assert", "await ")):
                    continue
                context_start = max(0, raw.rfind("\nfunc ", 0, match.start()))
                context = raw[context_start:match.start()]
                if re.search(r"\nfunc\s+(_ready|load_|boot_|_load)\b", context):
                    errors.append(
                        f"{rel}: push_error in boot/load path should be followed by return "
                        f"(near: {match.group(0)[:60]})"
                    )
    return checked


def check_typescript_files(errors: list[str]) -> int:
    if not MCP_TS_DIR.is_dir():
        return 0
    checked = 0
    for path in sorted(MCP_TS_DIR.rglob("*.ts")):
        if "node_modules" in path.parts:
            continue
        rel = path.relative_to(ROOT).as_posix()
        raw = path.read_text(encoding="utf-8")
        checked += 1
        for match in TS_SILENT_CATCH_RE.finditer(raw):
            body = match.group(1).strip()
            if not body or body in {"// noop", "/* noop */"}:
                lineno = raw[: match.start()].count("\n") + 1
                errors.append(
                    f"{rel}:{lineno}: silent catch block — use console.error or return MCP error"
                )
                continue
            if not TS_AUDIBLE_CATCH_RE.search(body):
                lineno = raw[: match.start()].count("\n") + 1
                errors.append(
                    f"{rel}:{lineno}: catch must log (console.error) or return structured error"
                )
    return checked


def main() -> int:
    errors: list[str] = []
    errors.extend(run_ruff_error_rules())
    check_python_files(errors)
    check_bash_scripts(errors)
    gd_count = check_gdscript_files(errors)
    ts_count = check_typescript_files(errors)

    if errors:
        print(f"[FAIL] L1_error_handling — {len(errors)} issue(s):", file=sys.stderr)
        for err in errors[:50]:
            print(f"  - {err}", file=sys.stderr)
        if len(errors) > 50:
            print(f"  … and {len(errors) - 50} more", file=sys.stderr)
        return 1

    parts = ["tools/**/*.py", "tools/*.sh"]
    if gd_count:
        parts.append(f"{gd_count} GDScript file(s)")
    if ts_count:
        parts.append(f"{ts_count} TypeScript file(s)")
    print(f"[PASS] L1_error_handling — {', '.join(parts)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
