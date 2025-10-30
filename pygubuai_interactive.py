#!/usr/bin/env python3
"""Interactive CLI prompts for PygubuAI"""
import sys

def prompt(question: str, default: str = "") -> str:
    """Simple text prompt"""
    if default:
        response = input(f"{question} [{default}]: ").strip()
        return response or default
    return input(f"{question}: ").strip()

def confirm(question: str, default: bool = True) -> bool:
    """Yes/no confirmation"""
    default_str = "Y/n" if default else "y/N"
    response = input(f"{question} [{default_str}]: ").strip().lower()
    
    if not response:
        return default
    return response in ['y', 'yes']

def select(question: str, options: list, default: int = 0) -> str:
    """Select from options"""
    print(f"\n{question}")
    for i, option in enumerate(options, 1):
        marker = "→" if i - 1 == default else " "
        print(f"  {marker} {i}. {option}")
    
    while True:
        try:
            choice = input(f"\nSelect [1-{len(options)}]: ").strip()
            if not choice:
                return options[default]
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return options[idx]
        except (ValueError, IndexError):
            pass
        print("Invalid selection, try again")

def interactive_create():
    """Interactive project creation"""
    print("🤖 PygubuAI Interactive Project Creator\n")
    
    name = prompt("Project name")
    if not name:
        print("Project name required")
        sys.exit(1)
    
    description = prompt("Describe your UI")
    if not description:
        print("Description required")
        sys.exit(1)
    
    register = confirm("Register project globally?", True)
    set_active = confirm("Set as active project?", True) if register else False
    
    return {
        "name": name,
        "description": description,
        "register": register,
        "set_active": set_active
    }
