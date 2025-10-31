#!/usr/bin/env python3
"""AI prompt template generator"""
from pathlib import Path
from typing import Optional
from .registry import Registry

PROMPT_TEMPLATES = {
    "add-feature": """Add the following feature to my pygubu project '{project}':

Feature: {feature}

Current project structure:
- UI file: {ui_file}
- Python file: {py_file}

Please:
1. Suggest the widgets needed
2. Provide the XML snippet for the UI file
3. Update the Python code with necessary callbacks
4. Maintain the existing layout and style

Keep changes minimal and focused on the requested feature.""",

    "fix-layout": """Fix the layout issues in my pygubu project '{project}'.

Current issues:
{issues}

Project files:
- UI: {ui_file}
- Code: {py_file}

Please analyze the current layout and suggest improvements for:
- Widget alignment
- Spacing and padding
- Responsive behavior
- Visual hierarchy

Provide specific XML changes needed.""",

    "refactor": """Refactor my pygubu project '{project}' to improve code quality.

Focus areas:
- Separate concerns (UI vs logic)
- Improve callback organization
- Add error handling
- Follow Python best practices

Project: {project_path}

Provide specific refactoring steps.""",

    "add-validation": """Add input validation to my pygubu project '{project}'.

Fields to validate:
{fields}

Requirements:
- Real-time validation feedback
- Clear error messages
- Visual indicators (colors, icons)
- Prevent invalid submissions

Provide both UI changes and validation code.""",

    "add-menu": """Add a menu bar to my pygubu project '{project}'.

Menu structure:
{menu_structure}

Include:
- File menu (New, Open, Save, Exit)
- Edit menu (if applicable)
- Help menu (About)
- Keyboard shortcuts

Provide XML for menu and Python callbacks.""",

    "improve-accessibility": """Improve accessibility in my pygubu project '{project}'.

Focus on:
- Keyboard navigation
- Screen reader support
- Color contrast
- Focus indicators
- ARIA labels

Analyze current UI and suggest improvements.""",
}


def generate_prompt(template_name: str, project_name: Optional[str] = None, **kwargs) -> str:
    """Generate AI prompt from template"""
    if template_name not in PROMPT_TEMPLATES:
        raise ValueError(f"Unknown template: {template_name}")

    # Get project info if provided
    if project_name:
        registry = Registry()
        project_path = registry.get_project(project_name)

        if project_path:
            project_dir = Path(project_path)
            kwargs.setdefault("project", project_name)
            kwargs.setdefault("project_path", str(project_dir))
            kwargs.setdefault("ui_file", str(project_dir / f"{project_name}.ui"))
            kwargs.setdefault("py_file", str(project_dir / f"{project_name}.py"))

    # Fill in defaults for missing values
    kwargs.setdefault("feature", "<describe feature>")
    kwargs.setdefault("issues", "<describe layout issues>")
    kwargs.setdefault("fields", "<list fields to validate>")
    kwargs.setdefault("menu_structure", "<describe menu structure>")

    return PROMPT_TEMPLATES[template_name].format(**kwargs)


def save_prompt(name: str, content: str):
    """Save prompt to Amazon Q prompts directory"""
    prompts_dir = Path.home() / ".amazonq" / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)

    prompt_file = prompts_dir / f"{name}.md"
    prompt_file.write_text(content)
    return prompt_file


def main():
    """CLI entry point"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: pygubu-prompt <template> [project] [args]")
        print("\\nAvailable templates:")
        for template in PROMPT_TEMPLATES.keys():
            print(f"  {template}")
        print("\\nCommands:")
        print("  list                    - List all templates")
        print("  <template> [project]    - Generate prompt")
        print("\\nExamples:")
        print("  pygubu-prompt add-feature myapp 'menu bar'")
        print("  pygubu-prompt fix-layout myapp")
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        print("\\nAvailable Prompt Templates:\\n")
        for template, content in PROMPT_TEMPLATES.items():
            first_line = content.split('\\n')[0]
            print(f"  {template:20} - {first_line}")
        print()
        return

    template_name = command
    project_name = sys.argv[2] if len(sys.argv) > 2 else None

    # Parse additional arguments
    kwargs = {}
    if len(sys.argv) > 3:
        if template_name == "add-feature":
            kwargs["feature"] = sys.argv[3]
        elif template_name == "fix-layout":
            kwargs["issues"] = sys.argv[3]
        elif template_name == "add-validation":
            kwargs["fields"] = sys.argv[3]
        elif template_name == "add-menu":
            kwargs["menu_structure"] = sys.argv[3]

    try:
        prompt = generate_prompt(template_name, project_name, **kwargs)
        print("\\n" + "="*60)
        print(prompt)
        print("="*60 + "\\n")

        # Offer to save
        if project_name:
            save_name = f"pygubu-{template_name}-{project_name}"
            print("TIP Tip: Save this prompt with:")
            print(f"   pygubu-prompt {template_name} {project_name} | save-as {save_name}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
