# Troubleshooting Guide

Complete troubleshooting guide for PygubuAI v0.8.0.

## Table of Contents

- [Quick Diagnostics](#quick-diagnostics)
- [Installation Issues](#installation-issues)
- [Command Issues](#command-issues)
- [Registry Issues](#registry-issues)
- [Project Issues](#project-issues)
- [Git Issues](#git-issues)
- [UI Issues](#ui-issues)
- [Performance Issues](#performance-issues)
- [Error Messages](#error-messages)

---

## Quick Diagnostics

### Health Check Script

```bash
#!/bin/bash
# Run this to diagnose common issues

echo "=== PygubuAI Health Check ==="

# Check Python version
echo -n "Python version: "
python3 --version

# Check PygubuAI installation
echo -n "PygubuAI installed: "
pip show pygubuai >/dev/null 2>&1 && echo "YES" || echo "NO"

# Check commands available
echo -n "pygubu-create: "
command -v pygubu-create >/dev/null 2>&1 && echo "OK" || echo "MISSING"

echo -n "pygubu-register: "
command -v pygubu-register >/dev/null 2>&1 && echo "OK" || echo "MISSING"

# Check registry
echo -n "Registry file: "
test -f ~/.pygubu-registry.json && echo "EXISTS" || echo "MISSING"

# Check dependencies
echo -n "pygubu: "
python3 -c "import pygubu" 2>/dev/null && echo "OK" || echo "MISSING"

echo -n "tkinter: "
python3 -c "import tkinter" 2>/dev/null && echo "OK" || echo "MISSING"

echo -n "rich: "
python3 -c "import rich" 2>/dev/null && echo "OK" || echo "MISSING"

echo "=== End Health Check ==="
```

Save as `health-check.sh` and run:
```bash
chmod +x health-check.sh
./health-check.sh
```

---

## Installation Issues

### Issue: Command not found

**Symptom:**
```bash
$ pygubu-create
bash: pygubu-create: command not found
```

**Diagnosis:**
```bash
# Check if installed
pip show pygubuai

# Check PATH
echo $PATH

# Find where installed
pip show -f pygubuai | grep Location
```

**Solutions:**

1. **Reinstall:**
```bash
pip uninstall pygubuai
pip install /path/to/PygubuAI
```

2. **Fix PATH:**
```bash
# Add to PATH
export PATH="$PATH:$HOME/.local/bin"

# Make permanent
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc
source ~/.bashrc
```

3. **Use full path:**
```bash
python3 -m pygubuai.cli.create myapp 'description'
```

### Issue: Import errors

**Symptom:**
```bash
ModuleNotFoundError: No module named 'pygubuai'
```

**Solutions:**

1. **Install in correct environment:**
```bash
# Check which Python
which python3

# Install for that Python
python3 -m pip install /path/to/PygubuAI
```

2. **Install dependencies:**
```bash
pip install pygubu pygubu-designer rich pydantic
```

3. **Use virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install /path/to/PygubuAI
```

### Issue: Permission denied

**Symptom:**
```bash
PermissionError: [Errno 13] Permission denied
```

**Solutions:**

1. **Install for user:**
```bash
pip install --user /path/to/PygubuAI
```

2. **Use virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install /path/to/PygubuAI
```

3. **Fix permissions:**
```bash
sudo chown -R $USER:$USER ~/.local
```

---

## Command Issues

### Issue: pygubu-create fails

**Symptom:**
```bash
$ pygubu-create myapp 'description'
Error: [ERROR] Failed to create project
```

**Diagnosis:**
```bash
# Check current directory permissions
ls -ld .

# Check disk space
df -h .

# Try with --dry-run
pygubu-create myapp 'description' --dry-run
```

**Solutions:**

1. **Check permissions:**
```bash
# Ensure write access
chmod u+w .
```

2. **Check disk space:**
```bash
df -h .
# Free up space if needed
```

3. **Use different directory:**
```bash
cd /tmp
pygubu-create myapp 'description'
```

### Issue: pygubu-register fails

**Symptom:**
```bash
$ pygubu-register list
Error: Failed to load registry
```

**Diagnosis:**
```bash
# Check registry file
ls -l ~/.pygubu-registry.json

# Check contents
cat ~/.pygubu-registry.json

# Validate JSON
python3 -m json.tool ~/.pygubu-registry.json
```

**Solutions:**

1. **Fix corrupted registry:**
```bash
# Backup
cp ~/.pygubu-registry.json ~/.pygubu-registry.json.backup

# Reinitialize
echo '{"projects": {}, "active_project": null}' > ~/.pygubu-registry.json
```

2. **Restore from backup:**
```bash
cp ~/.pygubu-registry.json.backup ~/.pygubu-registry.json
```

3. **Rebuild registry:**
```bash
# Remove corrupted file
rm ~/.pygubu-registry.json

# Scan for projects
pygubu-register scan ~/projects
```

---

## Registry Issues

### Issue: Project not found

**Symptom:**
```bash
Error: [ERROR] Project 'myapp' not found in registry
```

**Diagnosis:**
```bash
# List all projects
pygubu-register list

# Check if project exists
ls -d ~/projects/myapp
```

**Solutions:**

1. **Register project:**
```bash
pygubu-register add myapp ~/projects/myapp
```

2. **Scan directory:**
```bash
pygubu-register scan ~/projects
```

3. **Check spelling:**
```bash
# List projects to see correct name
pygubu-register list
```

### Issue: Registry corrupted

**Symptom:**
```bash
Error: Failed to parse registry file
```

**Solutions:**

1. **Validate JSON:**
```bash
python3 -m json.tool ~/.pygubu-registry.json
```

2. **Fix JSON errors:**
```bash
# Edit manually
nano ~/.pygubu-registry.json

# Or reinitialize
echo '{"projects": {}, "active_project": null}' > ~/.pygubu-registry.json
```

3. **Restore backup:**
```bash
cp ~/.pygubu-registry.json.backup ~/.pygubu-registry.json
```

### Issue: Duplicate projects

**Symptom:**
Multiple projects with same name in registry.

**Solutions:**

1. **Remove duplicate:**
```bash
pygubu-register remove myapp
pygubu-register add myapp /correct/path
```

2. **Edit registry manually:**
```bash
nano ~/.pygubu-registry.json
# Remove duplicate entry
```

---

## Project Issues

### Issue: UI file not found

**Symptom:**
```bash
Error: [ERROR] UI file not found: myapp.ui
```

**Diagnosis:**
```bash
# Check if file exists
ls -l myapp/myapp.ui

# Check project structure
tree myapp/
```

**Solutions:**

1. **Create UI file:**
```bash
cd myapp
pygubu-designer myapp.ui
```

2. **Check file name:**
```bash
# UI file should match project name
mv wrong_name.ui myapp.ui
```

3. **Regenerate project:**
```bash
cd ..
pygubu-create myapp 'description'
```

### Issue: Python file errors

**Symptom:**
```bash
$ python3 myapp.py
SyntaxError: invalid syntax
```

**Diagnosis:**
```bash
# Check Python syntax
python3 -m py_compile myapp.py

# Check imports
python3 -c "import pygubu"
```

**Solutions:**

1. **Fix syntax errors:**
```bash
# Use linter
python3 -m pylint myapp.py
```

2. **Regenerate Python file:**
```bash
# Backup first
cp myapp.py myapp.py.backup

# Regenerate
pygubu-create myapp 'description'
```

3. **Check dependencies:**
```bash
pip install pygubu tkinter
```

### Issue: UI/Code out of sync

**Symptom:**
Changes in UI file not reflected in Python code.

**Solutions:**

1. **Check sync status:**
```bash
pygubu-status myapp
```

2. **Manual sync:**
```bash
# Update Python code to match UI
# Add missing callbacks
# Update widget IDs
```

3. **Use watch mode:**
```bash
pygubu-ai-workflow watch myapp
```

---

## Git Issues

### Issue: Git not initialized

**Symptom:**
```bash
Error: Not a git repository
```

**Solutions:**

1. **Initialize Git:**
```bash
cd myapp
git init
git add .
git commit -m "Initial commit"
```

2. **Use --no-git flag:**
```bash
pygubu-create myapp 'description' --no-git
```

### Issue: Git commit fails

**Symptom:**
```bash
Error: Failed to create git commit
```

**Diagnosis:**
```bash
# Check Git status
git status

# Check Git config
git config user.name
git config user.email
```

**Solutions:**

1. **Configure Git:**
```bash
git config user.name "Your Name"
git config user.email "your@email.com"
```

2. **Manual commit:**
```bash
git add .
git commit -m "Your message"
```

---

## UI Issues

### Issue: UI doesn't display

**Symptom:**
Window opens but is blank or widgets missing.

**Diagnosis:**
```bash
# Check UI file
cat myapp.ui

# Validate XML
python3 -c "import xml.etree.ElementTree as ET; ET.parse('myapp.ui')"

# Check Python code
python3 myapp.py
```

**Solutions:**

1. **Validate UI XML:**
```bash
pygubu-validate myapp
```

2. **Check widget IDs:**
```bash
# Ensure IDs in UI match Python code
pygubu-inspect myapp
```

3. **Regenerate UI:**
```bash
pygubu-designer myapp.ui
```

### Issue: Tkinter errors

**Symptom:**
```bash
_tkinter.TclError: invalid command name
```

**Solutions:**

1. **Check tkinter installation:**
```bash
python3 -c "import tkinter; tkinter._test()"
```

2. **Install tkinter:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# macOS (usually included)
brew install python-tk
```

3. **Use different Python:**
```bash
# Try system Python
/usr/bin/python3 myapp.py
```

---

## Performance Issues

### Issue: Slow project creation

**Symptom:**
Project creation takes more than 5 seconds.

**Diagnosis:**
```bash
# Time the operation
time pygubu-create test 'test'

# Check disk I/O
iostat -x 1 5
```

**Solutions:**

1. **Use SSD:**
```bash
# Create projects on SSD
cd /path/to/ssd
pygubu-create myapp 'description'
```

2. **Disable Git:**
```bash
pygubu-create myapp 'description' --no-git
```

3. **Check disk space:**
```bash
df -h
```

### Issue: Slow registry operations

**Symptom:**
Registry commands take more than 1 second.

**Solutions:**

1. **Clean registry:**
```bash
# Remove old projects
pygubu-register remove old_project
```

2. **Rebuild registry:**
```bash
# Backup
cp ~/.pygubu-registry.json ~/.pygubu-registry.json.backup

# Reinitialize
echo '{"projects": {}, "active_project": null}' > ~/.pygubu-registry.json

# Scan only active projects
pygubu-register scan ~/active_projects
```

---

## Error Messages

### [ERROR] Path traversal detected

**Meaning:** Attempted to access files outside allowed directories.

**Solution:**
```bash
# Use relative paths within project
cd myproject
pygubu-create subproject 'description'

# Or use absolute paths without ".."
pygubu-create /full/path/to/project 'description'
```

### [ERROR] Invalid project name

**Meaning:** Project name contains invalid characters.

**Solution:**
```bash
# Use only letters, numbers, underscore, hyphen
pygubu-create my_project 'description'  # OK
pygubu-create my-project 'description'  # OK
pygubu-create "my<>project" 'description'  # INVALID
```

### [ERROR] File operation failed

**Meaning:** Failed to read/write file.

**Solutions:**
```bash
# Check permissions
ls -l file.txt
chmod u+rw file.txt

# Check disk space
df -h .

# Check file exists
ls -l file.txt
```

### [ERROR] Registry error

**Meaning:** Registry file corrupted or inaccessible.

**Solutions:**
```bash
# Reinitialize registry
echo '{"projects": {}, "active_project": null}' > ~/.pygubu-registry.json

# Or restore backup
cp ~/.pygubu-registry.json.backup ~/.pygubu-registry.json
```

### [ERROR] Validation error

**Meaning:** Input validation failed.

**Solutions:**
```bash
# Check input format
pygubu-create valid_name 'valid description'

# Avoid special characters
# Use alphanumeric, underscore, hyphen only
```

---

## Getting Help

### Debug Mode

```bash
# Enable debug output
export PYGUBU_DEBUG=1

# Run command
pygubu-create myapp 'description'

# Check logs
cat pygubu.log
```

### Verbose Output

```bash
# Run with verbose flag (if available)
pygubu-create myapp 'description' -v
```

### Collect Diagnostics

```bash
# Create diagnostic report
cat > diagnostics.txt <<EOF
Python version: $(python3 --version)
PygubuAI version: $(pip show pygubuai | grep Version)
OS: $(uname -a)
Registry: $(cat ~/.pygubu-registry.json)
Error: [paste error message]
EOF
```

### Report Issues

1. Run health check script
2. Collect diagnostics
3. Create GitHub issue: https://github.com/Teycir/PygubuAI/issues
4. Include:
   - Error message
   - Steps to reproduce
   - Diagnostics output
   - Expected vs actual behavior

---

## Common Solutions Summary

| Issue | Quick Fix |
|-------|-----------|
| Command not found | `pip install /path/to/PygubuAI` |
| Import error | `pip install pygubu rich pydantic` |
| Permission denied | `pip install --user /path/to/PygubuAI` |
| Registry corrupted | `echo '{"projects": {}, "active_project": null}' > ~/.pygubu-registry.json` |
| Project not found | `pygubu-register scan ~/projects` |
| UI file missing | `pygubu-designer myapp.ui` |
| Git not initialized | `git init && git add . && git commit -m "Initial"` |
| Tkinter missing | `sudo apt-get install python3-tk` |
| Slow performance | Use SSD, disable Git with `--no-git` |

---

## Prevention

### Best Practices

1. **Regular backups:**
```bash
cp ~/.pygubu-registry.json ~/.pygubu-registry.json.backup
```

2. **Use Git:**
```bash
git init
git add .
git commit -m "Checkpoint"
```

3. **Validate before deploy:**
```bash
pygubu-validate myapp
```

4. **Test in isolation:**
```bash
python3 -m venv test_env
source test_env/bin/activate
pip install /path/to/PygubuAI
```

5. **Keep updated:**
```bash
cd /opt/PygubuAI
git pull origin main
pip install --upgrade .
```

---

## Resources

- [User Guide](USER_GUIDE.md)
- [API Reference](API_REFERENCE.md)
- [Security Guide](SECURITY_GUIDE.md)
- [Deployment Guide](DEPLOYMENT_GUIDE.md)
- [GitHub Issues](https://github.com/Teycir/PygubuAI/issues)

---

**Version:** 0.8.0  
**Last Updated:** 2024
