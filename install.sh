#!/bin/bash
set -e

echo "🤖 Installing PygubuAI Tools..."

# Determine install location
if [ -w "/usr/local/bin" ]; then
    INSTALL_DIR="/usr/local/bin"
else
    INSTALL_DIR="$HOME/bin"
    mkdir -p "$INSTALL_DIR"
    
    # Add to PATH if not already there
    if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
        echo "export PATH=\"\$HOME/bin:\$PATH\"" >> "$HOME/.bashrc"
        echo "⚠️  Added $HOME/bin to PATH. Run: source ~/.bashrc"
    fi
fi

# Copy tools
cp pygubu-create "$INSTALL_DIR/"
cp pygubu-register "$INSTALL_DIR/"
cp pygubu-ai-workflow "$INSTALL_DIR/"
cp tkinter-to-pygubu "$INSTALL_DIR/"
cp pygubu-quickstart.py "$INSTALL_DIR/"

# Make executable
chmod +x "$INSTALL_DIR/pygubu-create"
chmod +x "$INSTALL_DIR/pygubu-register"
chmod +x "$INSTALL_DIR/pygubu-ai-workflow"
chmod +x "$INSTALL_DIR/tkinter-to-pygubu"
chmod +x "$INSTALL_DIR/pygubu-quickstart.py"

# Create AI context directory
mkdir -p "$HOME/.amazonq/prompts"

# Copy documentation
cp PYGUBUAI.md "$HOME/"
cp pygubuai-quickref.txt "$HOME/"

# Initialize registry
if [ ! -f "$HOME/.pygubu-registry.json" ]; then
    echo '{"projects": {}, "active_project": null, "last_updated": null}' > "$HOME/.pygubu-registry.json"
fi

echo ""
echo "✅ PygubuAI installed successfully!"
echo ""
echo "📁 Tools installed to: $INSTALL_DIR"
echo "📖 Documentation: ~/PYGUBUAI.md"
echo "📋 Quick ref: ~/pygubuai-quickref.txt"
echo ""
echo "🚀 Get started:"
echo "  pygubu-create myapp 'your app description'"
echo "  pygubu-register list"
echo ""
echo "📚 Read the docs: cat ~/PYGUBUAI.md"
