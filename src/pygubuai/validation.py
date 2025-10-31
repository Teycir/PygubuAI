"""Enhanced input validation and sanitization"""

import re
from pathlib import Path
from typing import Optional

RESERVED_NAMES = {
    "test",
    "tests",
    "src",
    "lib",
    "bin",
    "build",
    "dist",
    "venv",
    "env",
    "__pycache__",
    ".git",
    "node_modules",
}

MAX_NAME_LENGTH = 50
MIN_NAME_LENGTH = 2


def validate_project_name(name: str) -> tuple[bool, Optional[str]]:
    """Validate project name with detailed error messages"""
    if not name:
        return False, "Project name cannot be empty"

    if len(name) < MIN_NAME_LENGTH:
        return False, f"Project name must be at least {MIN_NAME_LENGTH} characters"

    if len(name) > MAX_NAME_LENGTH:
        return False, f"Project name must be at most {MAX_NAME_LENGTH} characters"

    if name.lower() in RESERVED_NAMES:
        return False, f"'{name}' is a reserved name"

    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_-]*$", name):
        return False, "Project name must start with letter and contain only letters, numbers, hyphens, underscores"

    if name.startswith("-") or name.startswith("_"):
        return False, "Project name cannot start with hyphen or underscore"

    return True, None


def sanitize_project_name(name: str) -> str:
    """Sanitize project name to valid format"""
    # Remove invalid characters
    name = re.sub(r"[^a-zA-Z0-9_-]", "_", name)

    # Ensure starts with letter
    if name and not name[0].isalpha():
        name = "project_" + name

    # Limit length
    if len(name) > MAX_NAME_LENGTH:
        name = name[:MAX_NAME_LENGTH]

    return name or "project"


def validate_path(path: str) -> tuple[bool, Optional[str]]:
    """Validate file path for security"""
    try:
        p = Path(path).resolve()

        # Check for path traversal
        if ".." in path:
            return False, "Path traversal not allowed"

        # Check for absolute paths outside allowed areas
        home = Path.home()
        cwd = Path.cwd()

        if not (str(p).startswith(str(home)) or str(p).startswith(str(cwd))):
            return False, "Path must be within home or current directory"

        return True, None
    except Exception as e:
        return False, f"Invalid path: {e}"


def validate_tags(tags: list) -> tuple[bool, Optional[str]]:
    """Validate project tags"""
    if not tags:
        return True, None

    if len(tags) > 10:
        return False, "Maximum 10 tags allowed"

    for tag in tags:
        if not tag or len(tag) > 20:
            return False, "Tags must be 1-20 characters"

        if not re.match(r"^[a-zA-Z0-9_-]+$", tag):
            return False, "Tags can only contain letters, numbers, hyphens, underscores"

    return True, None


def validate_description(description: str) -> tuple[bool, Optional[str]]:
    """Validate project description"""
    if not description:
        return True, None

    if len(description) > 500:
        return False, "Description must be at most 500 characters"

    return True, None
