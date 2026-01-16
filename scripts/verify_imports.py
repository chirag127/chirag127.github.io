#!/usr/bin/env python3
"""
Verify Imports - Static analysis to check for broken imports.
Scans all .py files in the project and verifies that imported modules exist.
"""

import ast
import os
import sys
from pathlib import Path
import re

# Setup paths
SCRIPT_DIR = Path(__file__).parent.absolute()
ROOT_DIR = SCRIPT_DIR.parent
sys.path.append(str(ROOT_DIR))

def get_all_python_files(root: Path):
    return [p for p in root.rglob("*.py") if ".venv" not in str(p) and "site-packages" not in str(p)]

def resolve_module(module_name: str, current_file: Path) -> bool:
    """
    Check if a module exists.
    Handles:
    - Standard library (assumed True if no exception, but we can't easily check strict stdlib without list)
    - Local src modules (src.core.config -> src/core/config.py)
    - Relative imports (..config -> ../config.py)
    """

    # 1. Ignore standard library / common packages (heuristic)
    # We allow these to pass for now, focusing on 'src' and local imports
    stdlib_and_libs = [
        "os", "sys", "json", "logging", "time", "pathlib", "typing", "subprocess", "shutil",
        "ast", "re", "argparse", "datetime", "threading", "random", "base64", "hashlib",
        "requests", "dotenv", "github", "tenacity", "colorama", "tqdm", "watchdog", "asyncio"
    ]

    root_module = module_name.split(".")[0]
    if root_module in stdlib_and_libs:
        return True

    # 2. Check strict local paths (src.X)
    if module_name.startswith("src."):
        # src.core.config -> src/core/config.py OR src/core/config/__init__.py
        rel_path = module_name.replace(".", "/")
        py_path = ROOT_DIR / f"{rel_path}.py"
        init_path = ROOT_DIR / rel_path / "__init__.py"

        return py_path.exists() or init_path.exists()

    # 3. Check relative imports
    if module_name.startswith("."):
        # This is hard to resolve statically without exact context,
        # but we can try basic resolution relative to current_file
        # This script won't perfectly resolve "..." but we can check mostly for breakage
        return True # Too complex to verify statically robustly in 100 lines, assume resolved if syntax is valid

    # 4. Unknown third party?
    # Assume valid if not starting with src. and not local
    return True

def check_file_imports(file_path: Path) -> list[str]:
    errors = []
    try:
        tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=str(file_path))
    except Exception as e:
        return [f"Syntax Error: {e}"]

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                # import src.core.config
                if alias.name.startswith("src."):
                    if not resolve_module(alias.name, file_path):
                        errors.append(f"Broken Import: '{alias.name}' not found")

        elif isinstance(node, ast.ImportFrom):
            # from src.core import config
            if node.module and node.module.startswith("src."):
                if not resolve_module(node.module, file_path):
                    errors.append(f"Broken From-Import: '{node.module}' not found")

            # from ..config import Settings
            if node.level > 0: # Relative import
                # We can do basic check: does the relative file exist?
                # current: src/clients/github.py
                # from ..config
                # path: src/clients/../config -> src/config

                # Logic:
                # level 1 (.) = same dir
                # level 2 (..) = parent

                parts = file_path.parent.parts
                # Remove 'level-1' parts from end
                # if level=1, remove 0
                # if level=2, remove 1

                base_dir = Path(*parts[:-(node.level-1)]) if node.level > 1 else file_path.parent

                if node.module:
                    # from ..config
                    target_module = node.module.replace(".", "/")
                    target_py = base_dir / f"{target_module}.py"
                    target_init = base_dir / target_module / "__init__.py"

                    if not (target_py.exists() or target_init.exists()):
                         # Check if checking from root (sometimes people mess up levels)
                         errors.append(f"Broken Relative Import: '{'.' * node.level}{node.module}' -> {target_py} (File missing)")
                else:
                    # from .. import something
                    # Just check valid directory
                    if not base_dir.exists():
                        errors.append(f"Broken Relative Path: level {node.level} from {file_path}")

    return errors

def main():
    output = []
    output.append("🔍 Starting Codebase Verification Scan...")
    output.append(f"📂 Root: {ROOT_DIR}")

    files = get_all_python_files(ROOT_DIR)
    output.append(f"📄 Found {len(files)} Python files.")

    error_count = 0
    files_with_errors = 0

    for f in files:
        errs = check_file_imports(f)
        if errs:
            files_with_errors += 1
            output.append(f"\n❌ {f.relative_to(ROOT_DIR)}")
            for e in errs:
                output.append(f"  - {e}")
                error_count += 1

    output.append("\n" + "="*40)
    if error_count == 0:
        output.append("✅ Scan Complete. 0 Broken Imports found.")
        success = True
    else:
        output.append(f"🛑 Scan Complete. {error_count} errors in {files_with_errors} files.")
        success = False

    report_file = ROOT_DIR / "verification_report.txt"
    report_file.write_text("\n".join(output), encoding="utf-8")
    print(f"Report written to {report_file}")

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
