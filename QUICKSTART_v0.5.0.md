# Quick Start Guide - PygubuAI v0.5.0

Get started with PygubuAI's new productivity features in 5 minutes!

## Installation

```bash
cd PygubuAI
pip install -e .
```

Verify installation:
```bash
python verify_v0.5.0.py
```

## 5-Minute Tour

### 1. Discover Widgets (30 seconds)

```bash
# See all available widgets
pygubu-widgets list

# Filter by category
pygubu-widgets list --category input

# Search for specific widgets
pygubu-widgets search "button"

# Get detailed info
pygubu-widgets info ttk.Button
```

**What you learned:** Browse 20+ widgets organized in 5 categories

---

### 2. Create and Preview (1 minute)

```bash
# Create a simple project
pygubu-create demo "form with name entry and submit button"

# Preview it instantly
pygubu-preview demo
```

**What you learned:** Create and preview UI without running full app

---

### 3. Check Status (30 seconds)

```bash
# Check project status
pygubu-status demo

# Make a change to the UI file
# (edit demo/demo.ui in any text editor)

# Check status again
pygubu-status demo
```

**What you learned:** Track sync status between UI and code

---

### 4. Generate Snippets (1 minute)

```bash
# Generate a button snippet
pygubu-snippet button "Save" --command on_save

# Generate an entry snippet
pygubu-snippet entry "Email" --variable email_var

# Generate a frame
pygubu-snippet frame --layout grid
```

**What you learned:** Quickly generate XML for common widgets

---

### 5. Validate and Inspect (1 minute)

```bash
# Validate the project
pygubu-validate demo

# Show widget tree
pygubu-inspect demo --tree

# Inspect specific widget
pygubu-inspect demo --widget mainwindow

# List callbacks
pygubu-inspect demo --callbacks
```

**What you learned:** Find issues and examine UI structure

---

### 6. Apply Themes (30 seconds)

```bash
# List available themes
pygubu-theme list

# Apply a theme
pygubu-theme demo clam

# Preview the change
pygubu-preview demo
```

**What you learned:** Change UI appearance with one command

---

### 7. AI Prompts (30 seconds)

```bash
# List prompt templates
pygubu-prompt list

# Generate a prompt for adding features
pygubu-prompt add-feature demo "menu bar with File and Help"

# Copy the output and paste to your AI assistant!
```

**What you learned:** Get optimized prompts for AI collaboration

---

### 8. Export Standalone (30 seconds)

```bash
# Export to standalone file
pygubu-export demo

# Run the standalone version
python demo/demo_standalone.py
```

**What you learned:** Create single-file distributions

---

## Common Workflows

### Design Workflow

```bash
# 1. Create project
pygubu-create myapp "your description"

# 2. Start preview in watch mode
pygubu-preview myapp --watch &

# 3. Edit in Designer (preview updates automatically)
pygubu-designer myapp/myapp.ui

# 4. Validate when done
pygubu-validate myapp
```

### Multi-Project Management

```bash
# Apply theme to all projects
pygubu-batch update-theme clam

# Validate all projects
pygubu-batch validate

# Check status of each
for proj in $(pygubu-register list | tail -n +2); do
    pygubu-status $proj
done
```

### Widget Discovery

```bash
# Find input widgets
pygubu-widgets list --category input

# Get details on one
pygubu-widgets info ttk.Entry

# Generate snippet
pygubu-snippet entry "Username"

# Paste into Designer or UI file
```

## Next Steps

1. **Read the Feature Showcase:**
   ```bash
   cat FEATURE_SHOWCASE.md
   ```

2. **Try Advanced Features:**
   - Batch operations: `pygubu-batch --help`
   - Widget inspection: `pygubu-inspect --help`
   - AI prompts: `pygubu-prompt --help`

3. **Check the Roadmap:**
   ```bash
   cat ROADMAP.md
   ```

4. **Run Tests:**
   ```bash
   python run_tests.py
   ```

## Cheat Sheet

```bash
# Status & Info
pygubu-status [project]              # Check sync status
pygubu-widgets list                  # Browse widgets
pygubu-inspect [project] --tree      # Show structure

# Preview & Validate
pygubu-preview [project] --watch     # Live preview
pygubu-validate [project]            # Check issues

# Generate & Create
pygubu-snippet [widget] [text]       # Generate XML
pygubu-prompt [template] [project]   # AI prompts

# Modify & Export
pygubu-theme [project] [theme]       # Apply theme
pygubu-export [project]              # Standalone file

# Batch Operations
pygubu-batch update-theme [theme]    # Theme all projects
pygubu-batch validate                # Validate all
```

## Tips

1. **Use watch mode for design:**
   ```bash
   pygubu-preview myapp --watch
   ```

2. **Validate before commits:**
   ```bash
   pygubu-validate myapp && git commit
   ```

3. **Keep widget reference open:**
   ```bash
   pygubu-widgets list --category input > widgets.txt
   ```

4. **Generate prompts for AI:**
   ```bash
   pygubu-prompt add-feature myapp "feature description"
   ```

5. **Quick theme testing:**
   ```bash
   for theme in clam alt classic; do
       pygubu-theme myapp $theme
       pygubu-preview myapp
   done
   ```

## Help

Every command has built-in help:
```bash
pygubu-status --help
pygubu-widgets --help
pygubu-preview --help
# ... etc
```

## Troubleshooting

**Command not found?**
```bash
pip install -e .
```

**Import errors?**
```bash
python verify_v0.5.0.py
```

**Need pygubu?**
```bash
pip install pygubu pygubu-designer
```

---

**Ready to build amazing Tkinter UIs! 🚀**

For more details, see:
- [FEATURE_SHOWCASE.md](FEATURE_SHOWCASE.md) - Detailed examples
- [ROADMAP.md](ROADMAP.md) - Implementation details
- [README.md](README.md) - Full documentation
