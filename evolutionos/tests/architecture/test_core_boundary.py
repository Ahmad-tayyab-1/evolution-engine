"""
Architecture Test: Core Boundary Rule (EC-BND-001).

Enforces that `evolutionos/core` modules never import from or reference any
platform-specific or execution layer concepts (YouTube, video rendering, ffmpeg,
LLM provider details, etc.).
"""
import os
import glob
import ast


def test_core_has_no_execution_imports():
    """EC-BND-001: Core must never import execution layer concepts or platforms."""
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "core"))
    core_files = glob.glob(os.path.join(root_dir, "**", "*.py"), recursive=True)

    forbidden_terms = [
        "execution", "youtube", "video", "thumbnail", "render",
        "publish", "narration", "pipeline", "ffmpeg", "groq",
        "openai", "gemini", "shorts", "pollinations", "deepgram"
    ]

    violations = []

    for file_path in core_files:
        if os.path.basename(file_path) == "__init__.py":
            continue
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            source = f.read()

        # Check raw text / lower for forbidden terms in code/imports
        try:
            tree = ast.parse(source, filename=file_path)
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    # Check import names
                    module_name = getattr(node, "module", "") or ""
                    names = [alias.name for alias in getattr(node, "names", [])]
                    full_imports_text = f"{module_name} {' '.join(names)}".lower()
                    for term in forbidden_terms:
                        if term in full_imports_text:
                            violations.append(
                                f"File {file_path} imports forbidden term '{term}': {full_imports_text}"
                            )
        except SyntaxError as e:
            violations.append(f"SyntaxError parsing {file_path}: {e}")

        # Check raw string matching in lower-case source excluding comments/docstrings where appropriate
        in_docstring = False
        for line_num, line in enumerate(source.splitlines(), 1):
            stripped = line.strip().lower()
            if '"""' in stripped or "'''" in stripped:
                # Toggle docstring state or single-line docstring
                if stripped.count('"""') == 1 or stripped.count("'''") == 1:
                    in_docstring = not in_docstring
                continue
            if in_docstring or stripped.startswith("#"):
                continue

            for term in forbidden_terms:
                if f"import {term}" in stripped or f"from {term}" in stripped:
                    violations.append(
                        f"File {os.path.relpath(file_path)} (line {line_num}) violates EC-BND-001 with '{term}': {line.strip()}"
                    )
                elif f".{term}" in stripped:
                    # Allow .publish() only on event brokers (domain event emitting), forbid platform publishing
                    if term == "publish" and ("broker.publish" in stripped or "self.broker.publish" in stripped):
                        continue
                    violations.append(
                        f"File {os.path.relpath(file_path)} (line {line_num}) violates EC-BND-001 with attribute '.{term}': {line.strip()}"
                    )

    assert not violations, "Core boundary violations found:\n" + "\n".join(violations)
