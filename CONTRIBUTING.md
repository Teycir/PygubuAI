# Contributing to PygubuAI

Thank you for your interest in contributing to PygubuAI!

## Development Setup

### 1. Clone and Install Dependencies

```bash
git clone https://github.com/yourusername/pygubuai.git
cd pygubuai

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install pygubu pygubu-designer
```

### 2. Run Tools Without Installing

```bash
# Run tools directly from repo
./pygubu-create mytest 'test app with button'
./pygubu-register list
./pygubu-ai-workflow watch mytest

# Or add to PATH temporarily
export PATH="$PWD:$PATH"
pygubu-create mytest 'test app'
```

### 3. Test Your Changes

```bash
# Test project creation
./pygubu-create testapp 'login form with username and password'
cd testapp
python testapp.py

# Test registration
./pygubu-register add testapp
./pygubu-register list
```

## Project Structure

```
pygubuai/
├── pygubu-create           # Project creation wrapper
├── pygubu-quickstart.py    # Core project generator
├── pygubu-register         # Project registry manager
├── pygubu-ai-workflow      # Watch mode for UI changes
├── tkinter-to-pygubu       # Converter (placeholder)
├── install.sh              # Installation script
├── .amazonq/prompts/       # AI context files
└── examples/               # Example projects
```

## Making Changes

### Adding Features

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make your changes
3. Test thoroughly
4. Submit a pull request

### Improving AI Generation

The `pygubu-create` tool uses simple keyword matching in `parse_description()`. To improve:

1. Add more widget detection patterns
2. Implement layout inference (grid vs pack)
3. Add support for more complex UI patterns
4. Consider integrating actual LLM API calls

### Enhancing Watch Mode

The `pygubu-ai-workflow` tool currently detects changes via file hashing. Improvements:

1. Parse XML to detect specific widget changes
2. Generate more specific AI prompts
3. Auto-suggest code modifications
4. Integrate with version control

## Code Style

- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

## Testing

Before submitting:

```bash
# Test all commands
./pygubu-create test1 'simple app with button'
./pygubu-register scan .
./pygubu-register active test1
./pygubu-ai-workflow watch test1  # Ctrl+C to stop
```

## Documentation

- Update README.md for user-facing changes
- Update PYGUBUAI.md for detailed documentation
- Add examples for new features

## Questions?

Open an issue for discussion before major changes.
