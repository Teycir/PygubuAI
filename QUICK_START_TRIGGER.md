# PygubuAI - Quick Start with Trigger Word

## Setup Complete!

Your /home/teycir/Repos directory is now PygubuAI-enabled.

## How to Use (From Any Directory)

Just mention "pygubuai" in your Amazon Q chat:

### Create New Projects

```
pygubuai create a login form
pygubuai build a todo app with add and delete buttons
pygubuai make a dashboard with charts and tables
```

### Modify Existing Projects

```
pygubuai add a submit button
pygubuai change the background color to blue
pygubuai add validation to the email field
```

### Project Management

```
pygubuai show my projects
pygubuai switch to login project
pygubuai what's the status of my project
```

### Sync After Manual Changes

```
pygubuai I changed the UI in Designer, sync the code
pygubuai update the Python code to match my UI
```

## That's It!

No commands to memorize. Just say "pygubuai" + what you want.

## Examples

**You:** pygubuai create a settings panel with theme dropdown and font size slider

**Amazon Q:** Creates complete project with:
- settings.ui (XML with Combobox and Scale widgets)
- settings.py (Python code with callbacks)
- Registered in ~/.pygubu-registry.json

**You:** pygubuai add a save button at the bottom

**Amazon Q:** Updates both .ui and .py files with new button

**You:** (Make visual changes in Pygubu Designer)

**You:** pygubuai sync my changes

**Amazon Q:** Regenerates Python code to match your UI changes

## Marked Directories

The following directories now have .pygubuai markers:
- /home/teycir/Repos/PygubuAI (main repo)
- /home/teycir/Repos/PygubuAI/examples/* (all examples)
- /home/teycir/Repos/pygubu (pygubu library)
- Any directory with .ui files in /home/teycir/Repos

## Add More Directories

```bash
cd /home/teycir/Repos/PygubuAI
bash scripts/setup-trigger.sh mark /path/to/new/project
```

Or scan another directory:
```bash
bash scripts/setup-trigger.sh scan /path/to/projects
```

## What Happens Behind the Scenes

1. You say "pygubuai" in chat
2. Amazon Q loads PygubuAI context
3. Checks for .pygubuai marker in current directory
4. Loads project registry
5. Understands your natural language
6. Executes appropriate commands
7. Shows you the results

You never see the commands - just natural conversation.
