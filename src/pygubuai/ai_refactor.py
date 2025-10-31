#!/usr/bin/env python3
"""AI-powered refactoring suggestions"""
import json
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass, asdict

@dataclass
class Suggestion:
    id: str
    category: str
    title: str
    description: str
    impact: str
    effort: str
    auto_fixable: bool

def analyze_refactoring_opportunities(project_name: str) -> List[Suggestion]:
    """Analyze project for refactoring opportunities"""
    from .registry import Registry
    from .ai_analyzer import analyze_project

    registry = Registry()
    project_path = registry.get_project(project_name)

    if not project_path:
        return []

    analysis = analyze_project(project_name)
    suggestions = []

    suggestions.extend(_check_widget_consolidation(analysis))
    suggestions.extend(_check_layout_optimization(analysis))
    suggestions.extend(_check_accessibility(analysis))
    suggestions.extend(_check_performance(analysis))
    suggestions.extend(_check_code_quality(analysis))

    return suggestions

def _check_widget_consolidation(analysis: Dict) -> List[Suggestion]:
    """Check for widget consolidation opportunities"""
    suggestions = []
    widget_types = analysis.get("widget_types", {})

    if widget_types.get("ttk.Label", 0) > 10:
        suggestions.append(Suggestion(
            id="consolidate_labels",
            category="layout",
            title="Consolidate Labels",
            description=f"Found {widget_types['ttk.Label']} labels. Consider using frames or labelframes to group related labels.",
            impact="medium",
            effort="low",
            auto_fixable=False
        ))

    if widget_types.get("ttk.Button", 0) > 5:
        suggestions.append(Suggestion(
            id="button_toolbar",
            category="layout",
            title="Create Button Toolbar",
            description=f"Found {widget_types['ttk.Button']} buttons. Consider grouping into a toolbar frame.",
            impact="medium",
            effort="low",
            auto_fixable=False
        ))

    return suggestions

def _check_layout_optimization(analysis: Dict) -> List[Suggestion]:
    """Check for layout optimization opportunities"""
    suggestions = []
    layouts = analysis.get("layout_patterns", [])

    if len(layouts) > 2:
        suggestions.append(Suggestion(
            id="simplify_layout",
            category="layout",
            title="Simplify Layout Strategy",
            description=f"Using {len(layouts)} different layout managers. Stick to 1-2 for consistency.",
            impact="high",
            effort="medium",
            auto_fixable=False
        ))

    if "pack" in layouts and "grid" in layouts:
        suggestions.append(Suggestion(
            id="mixed_layout",
            category="layout",
            title="Mixed Layout Managers",
            description="Mixing pack and grid can cause issues. Use grid for complex layouts.",
            impact="high",
            effort="medium",
            auto_fixable=False
        ))

    return suggestions

def _check_accessibility(analysis: Dict) -> List[Suggestion]:
    """Check for accessibility improvements"""
    suggestions = []
    widget_types = analysis.get("widget_types", {})

    entry_count = widget_types.get("ttk.Entry", 0)
    label_count = widget_types.get("ttk.Label", 0)

    if entry_count > 0 and label_count < entry_count:
        suggestions.append(Suggestion(
            id="add_labels",
            category="accessibility",
            title="Add Labels for Inputs",
            description=f"Found {entry_count} entries but only {label_count} labels. Add descriptive labels.",
            impact="high",
            effort="low",
            auto_fixable=False
        ))

    if widget_types.get("ttk.Button", 0) > 0:
        suggestions.append(Suggestion(
            id="keyboard_shortcuts",
            category="accessibility",
            title="Add Keyboard Shortcuts",
            description="Consider adding keyboard shortcuts (accelerators) for buttons.",
            impact="medium",
            effort="low",
            auto_fixable=False
        ))

    return suggestions

def _check_performance(analysis: Dict) -> List[Suggestion]:
    """Check for performance improvements"""
    suggestions = []

    if analysis.get("widget_count", 0) > 50:
        suggestions.append(Suggestion(
            id="lazy_loading",
            category="performance",
            title="Consider Lazy Loading",
            description=f"Large widget count ({analysis['widget_count']}). Consider lazy loading or pagination.",
            impact="high",
            effort="high",
            auto_fixable=False
        ))

    return suggestions

def _check_code_quality(analysis: Dict) -> List[Suggestion]:
    """Check for code quality improvements"""
    suggestions = []

    if not analysis.get("has_docstrings"):
        suggestions.append(Suggestion(
            id="add_docstrings",
            category="quality",
            title="Add Documentation",
            description="No docstrings found. Add module and function documentation.",
            impact="medium",
            effort="low",
            auto_fixable=True
        ))

    if analysis.get("callback_count", 0) == 0:
        suggestions.append(Suggestion(
            id="add_handlers",
            category="quality",
            title="Add Event Handlers",
            description="No callbacks found. Add event handlers for user interactions.",
            impact="high",
            effort="medium",
            auto_fixable=False
        ))

    widget_types = analysis.get("widget_types", {})
    if any("tk." in wt and wt != "tk.Toplevel" for wt in widget_types):
        suggestions.append(Suggestion(
            id="use_ttk",
            category="quality",
            title="Migrate to ttk Widgets",
            description="Using legacy tk widgets. Migrate to themed ttk widgets.",
            impact="medium",
            effort="medium",
            auto_fixable=True
        ))

    return suggestions

def save_suggestions(project_name: str, suggestions: List[Suggestion]):
    """Save suggestions to file"""
    output_dir = Path.home() / ".amazonq" / "prompts"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{project_name}-suggestions.json"
    data = {
        "project": project_name,
        "suggestions": [asdict(s) for s in suggestions]
    }

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

    return output_file

def main():
    """CLI entry point"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: pygubu-ai-refactor <project>")
        sys.exit(1)

    project_name = sys.argv[1]
    suggestions = analyze_refactoring_opportunities(project_name)

    if not suggestions:
        print(f"No refactoring suggestions for '{project_name}'")
        sys.exit(0)

    print(f"Refactoring Suggestions for '{project_name}':\n")

    for i, sug in enumerate(suggestions, 1):
        print(f"{i}. [{sug.category.upper()}] {sug.title}")
        print(f"   {sug.description}")
        print(f"   Impact: {sug.impact} | Effort: {sug.effort} | Auto-fix: {sug.auto_fixable}")
        print()

    output_file = save_suggestions(project_name, suggestions)
    print(f"Suggestions saved to: {output_file}")

if __name__ == "__main__":
    main()
