# PygubuAI Trigger Setup - Simple Activation

## What This Does

Enables you to use "pygubuai" keyword from ANY directory to activate PygubuAI context in Amazon Q.

## One-Time Setup (2 minutes)

### Step 1: Mark Your Project Directories

Choose one option:

#### Option A: Mark all existing pygubu projects in /home/teycir/Repos
```bash
cd /home/teycir/Repos/PygubuAI
./scripts/setup-trigger.sh scan /home/teycir/Repos
```

#### Option B: Mark a specific project directory
```bash
cd /home/teycir/Repos/PygubuAI
./scripts/setup-trigger.sh mark /path/to/your/project
```

#### Option C: Mark PygubuAI repo itself
```bash
cd /home/teycir/Repos/PygubuAI
./scripts/setup-trigger.sh self
```

### Step 2: Verify Setup

Check that .pygubuai marker files were created:
```bash
find /home/teycir/Repos -name ".pygubuai"
```

## How to Use

### From ANY marked directory, just say:

**Create new project:**
```
pygubuai create a login form with username and password
```

**Add to existing project:**
```
pygubuai add a submit button
```

**Show projects:**
```
pygubuai show my projects
```

**Build complex UI:**
```
pygubuai create a dashboard with revenue chart, top products list, and search bar
```

**Sync after manual changes:**
```
pygubuai I changed the UI in Designer, sync the code
```

## What Happens Behind the Scenes

1. Amazon Q detects "pygubuai" keyword
2. Loads PygubuAI context automatically
3. Checks for .pygubuai marker in current directory
4. Loads project registry from ~/.pygubu-registry.json
5. Understands your natural language request
6. Executes appropriate pygubu commands
7. Shows you the results

## No Commands to Memorize

You never need to remember:
- pygubu-create syntax
- pygubu-register commands
- File paths
- XML structure
- Python boilerplate

Just say "pygubuai" + what you want in plain English.

## Examples

### Example 1: New Project
```
You: pygubuai create a todo app
Q: Creating todo app...
   Created at: /home/teycir/Repos/todo/
   Files: todo.ui, todo.py
   Run with: python3 todo.py
```

### Example 2: Modify Existing
```
You: pygubuai add a delete button with red background
Q: Added delete button to your active project.
   Updated: myapp.ui, myapp.py
```

### Example 3: Project Management
```
You: pygubuai what projects do I have
Q: You have 3 registered projects:
   - todo (/home/teycir/Repos/todo)
   - login (/home/teycir/Repos/login)
   - dashboard (/home/teycir/Repos/dashboard)
```

### Example 4: Complex UI
```
You: pygubuai build a settings panel with theme dropdown, font size slider, and save button
Q: Creating settings panel...
   Added widgets: Combobox (theme), Scale (font size), Button (save)
   Created at: /home/teycir/Repos/settings/
```

## Troubleshooting

### "pygubuai" not recognized?
- Make sure you ran setup-trigger.sh
- Check .pygubuai file exists in your directory
- Try mentioning @pygubu-context first

### Commands not working?
- Verify PygubuAI is installed: `pygubu-create --version`
- Check registry exists: `cat ~/.pygubu-registry.json`
- Run: `pygubu-register scan /home/teycir/Repos`

## Advanced: Mark New Projects Automatically

Add to your shell profile (~/.bashrc or ~/.zshrc):
```bash
alias pygubu-init='touch .pygubuai && echo "PygubuAI enabled in $(pwd)"'
```

Then in any new project directory:
```bash
pygubu-init
```

## Next Steps

1. Run setup script to mark your directories
2. Open Amazon Q chat
3. Navigate to any marked directory
4. Say "pygubuai create..." and watch it work!

No more command memorization. Just natural conversation.
