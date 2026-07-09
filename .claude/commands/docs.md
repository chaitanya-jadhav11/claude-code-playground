---
description: Automatically add docstrings and type hints to a Python file.
argument-hint: [file_path]
---

Analyze the Python file at $ARGUMENTS.
Without changing the underlying logic:
1. Add PEP 257 compliant docstrings to all classes and functions.
2. Add explicit Python type hints to all function signatures.
Show the diff and ask for permission before modifying the file.
