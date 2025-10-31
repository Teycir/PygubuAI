#!/usr/bin/env python3
"""Natural language queries for project analysis"""
import re
from typing import Dict, Any

def query_project(project_name: str, query: str) -> str:
    """Answer natural language queries about project"""
    from .ai_analyzer import analyze_project
    from .ai_context import generate_context

    analysis = analyze_project(project_name)
    context = generate_context(project_name)

    if "error" in analysis:
        return f"Error: {analysis['error']}"

    query_lower = query.lower()

    patterns = [
        (r'how many (widgets?|buttons?|entries?|labels?)', _count_widgets),
        (r'what (callbacks?|handlers?|events?)', _list_callbacks),
        (r'(unused|missing) (callbacks?|handlers?)', _find_unused),
        (r'complexity|complex', _get_complexity),
        (r'suggestions?|improvements?|recommendations?', _get_suggestions),
        (r'layout|manager', _get_layout_info),
        (r'widget types?|what widgets', _list_widget_types),
    ]

    for pattern, handler in patterns:
        if re.search(pattern, query_lower):
            return handler(analysis, context, query_lower)

    return "I don't understand that query. Try: 'How many widgets?', 'What callbacks?', 'Show complexity'"


def _count_widgets(analysis: Dict, context: Dict, query: str) -> str:
    """Count widgets"""
    if 'button' in query:
        count = analysis['widget_types'].get('ttk.Button', 0) + analysis['widget_types'].get('tk.Button', 0)
        return f"Found {count} buttons"
    elif 'entry' in query or 'entries' in query:
        count = analysis['widget_types'].get('ttk.Entry', 0) + analysis['widget_types'].get('tk.Entry', 0)
        return f"Found {count} entry widgets"
    elif 'label' in query:
        count = analysis['widget_types'].get('ttk.Label', 0) + analysis['widget_types'].get('tk.Label', 0)
        return f"Found {count} labels"
    else:
        return f"Total widgets: {analysis['widget_count']}"


def _list_callbacks(analysis: Dict, context: Dict, query: str) -> str:
    """List callbacks"""
    callbacks = context.get('callbacks', [])
    if not callbacks:
        return "No callbacks found"

    return f"Callbacks ({len(callbacks)}):\n" + "\n".join(f"- {cb}" for cb in callbacks)


def _find_unused(analysis: Dict, context: Dict, query: str) -> str:
    """Find unused callbacks"""
    return "Unused callback detection requires code analysis (coming soon)"


def _get_complexity(analysis: Dict, context: Dict, query: str) -> str:
    """Get complexity score"""
    score = analysis['complexity']
    level = "low" if score < 5 else "medium" if score < 10 else "high"
    return f"Complexity: {score}/10 ({level})\n" \
           f"Widgets: {analysis['widget_count']}\n" \
           f"Callbacks: {analysis['callback_count']}\n" \
           f"Layouts: {', '.join(analysis['layout_patterns'])}"


def _get_suggestions(analysis: Dict, context: Dict, query: str) -> str:
    """Get improvement suggestions"""
    suggestions = analysis.get('suggestions', [])
    if not suggestions:
        return "No suggestions - project looks good!"

    return "Suggestions:\n" + "\n".join(f"- {s}" for s in suggestions)


def _get_layout_info(analysis: Dict, context: Dict, query: str) -> str:
    """Get layout information"""
    layouts = analysis.get('layout_patterns', [])
    if not layouts:
        return "No layout managers detected"

    return f"Layout managers: {', '.join(layouts)}"


def _list_widget_types(analysis: Dict, context: Dict, query: str) -> str:
    """List widget types"""
    types = analysis.get('widget_types', {})
    if not types:
        return "No widgets found"

    lines = ["Widget types:"]
    for wtype, count in sorted(types.items(), key=lambda x: -x[1]):
        lines.append(f"- {wtype}: {count}")

    return "\n".join(lines)


def main():
    """CLI entry point"""
    import sys

    if len(sys.argv) < 3:
        print("Usage: pygubu-ai-query <project> '<query>'")
        print("\nExample queries:")
        print("  'How many widgets?'")
        print("  'What callbacks are defined?'")
        print("  'Show complexity'")
        print("  'What are the suggestions?'")
        sys.exit(1)

    project_name = sys.argv[1]
    query = " ".join(sys.argv[2:])

    result = query_project(project_name, query)
    print(result)

if __name__ == "__main__":
    main()
