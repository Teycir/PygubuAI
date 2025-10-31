#!/bin/bash
set -e

echo "🗑️  Uninstalling PygubuAI Tools..."

# Determine install location
if [ -w "/usr/local/bin" ]; then
    INSTALL_DIR="/usr/local/bin"
else
    INSTALL_DIR="$HOME/bin"
fi

# Remove tools
for tool in pygubu-create pygubu-register pygubu-ai-workflow tkinter-to-pygubu pygubu-quickstart.py pygubu-template; do
    if [ -f "$INSTALL_DIR/$tool" ]; then
        rm "$INSTALL_DIR/$tool"
        echo "  Removed $tool"
    fi
done

# Remove modules
for module in pygubuai_config.py pygubuai_errors.py pygubuai_interactive.py pygubuai_widgets.py pygubuai_templates.py; do
    if [ -f "$INSTALL_DIR/$module" ]; then
        rm "$INSTALL_DIR/$module"
        echo "  Removed $module"
    fi
done

echo ""
echo "✅ PygubuAI uninstalled"
echo ""
echo "⚠️  Kept user data:"
echo "  - ~/.pygubu-registry.json (project registry)"
echo "  - ~/.amazonq/prompts/pygubu-context.md (AI context)"
echo "  - ~/PYGUBUAI.md (documentation)"
echo ""
echo "To remove user data: rm ~/.pygubu-registry.json ~/.amazonq/prompts/pygubu-context.md ~/PYGUBUAI.md"
