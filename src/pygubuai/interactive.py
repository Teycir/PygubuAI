"""Interactive CLI prompts for project creation"""
import sys
from typing import Optional, List


def prompt(message: str, default: Optional[str] = None) -> str:
    """Prompt user for input with optional default"""
    if default:
        message = f"{message} [{default}]"
    message += ": "
    
    try:
        response = input(message).strip()
        return response if response else (default or "")
    except (KeyboardInterrupt, EOFError):
        print("\n\nCancelled.")
        sys.exit(0)


def confirm(message: str, default: bool = True) -> bool:
    """Ask yes/no question"""
    suffix = " [Y/n]" if default else " [y/N]"
    response = prompt(message + suffix, "").lower()
    
    if not response:
        return default
    return response in ('y', 'yes')


def choose(message: str, options: List[str], default: Optional[str] = None) -> str:
    """Choose from list of options"""
    print(f"\n{message}")
    for i, option in enumerate(options, 1):
        marker = " (default)" if option == default else ""
        print(f"  {i}. {option}{marker}")
    
    while True:
        choice = prompt("Enter number", str(options.index(default) + 1) if default else None)
        
        if not choice and default:
            return default
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return options[idx]
        except ValueError:
            pass
        
        print("Invalid choice. Try again.")


def interactive_create() -> dict:
    """Interactive project creation wizard"""
    print("\n PygubuAI Interactive Project Creator\n")
    
    name = prompt("Project name", "myapp")
    description = prompt("Description (e.g., 'login form with username and password')")
    
    use_template = confirm("Use a template?", False)
    template = None
    if use_template:
        templates = ["login", "crud", "settings", "dashboard", "wizard", "none"]
        template = choose("Select template", templates, "none")
        if template == "none":
            template = None
    
    init_git = confirm("Initialize Git repository?", True)
    
    return {
        "name": name,
        "description": description,
        "template": template,
        "git": init_git
    }
