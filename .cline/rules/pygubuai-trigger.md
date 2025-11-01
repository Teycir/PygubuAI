# PygubuAI Auto-Trigger Rule for Cline

## Activation Keyword: "pygubuai"

When the user mentions the word "pygubuai" (case-insensitive) in ANY message from ANY directory, automatically activate PygubuAI context and capabilities.

## Auto-Detection

1. Check if current directory or any parent directory contains `.pygubuai` marker file
2. If found, treat as PygubuAI-enabled project
3. Load project context automatically

## Automatic Actions When Triggered

1. Load the pygubu-context prompt knowledge
2. Check for project registry at ~/.pygubu-registry.json
3. Detect if current directory is a registered project
4. Load active project context if available
5. Enable natural language UI creation mode

## Natural Language Understanding

When user says things like:
- "pygubuai create a login form"
- "use pygubuai to build a dashboard"
- "pygubuai add a button"
- "with pygubuai make a settings panel"

Automatically:
- Parse the intent (create, modify, add, etc.)
- Identify the UI components needed
- Use pygubu-create or appropriate tools
- Generate both .ui and .py files
- Register the project
- Provide next steps

## Project Context Loading

When triggered, automatically load:
- Current directory path
- Existing .ui files in directory
- Existing .py files that use pygubu
- Project registry information
- Active project status

## Response Pattern

When "pygubuai" is mentioned:
1. Acknowledge PygubuAI mode is active
2. Show current project context (if any)
3. Ask for clarification if intent is unclear
4. Execute the requested action
5. Provide file locations and next steps

## Integration with Existing Projects

If user is in /home/teycir/Repos or any subdirectory:
- Scan for .pygubuai marker files
- Auto-detect pygubu projects (.ui files)
- Offer to register unregistered projects
- Set as active project if requested

## Example Interactions

User: "pygubuai create todo app"
Response: [Creates project using pygubu-create, shows files created]

User: "pygubuai show my projects"
Response: [Lists all registered projects from registry]

User: "pygubuai I need a form with name and email"
Response: [Creates form scaffold with those fields]

User: "pygubuai sync my UI changes"
Response: [Detects .ui changes, updates Python code]

## No Command Memorization Required

User never needs to remember:
- pygubu-create syntax
- pygubu-register commands
- File paths or structures
- XML format
- Python boilerplate

Just say "pygubuai" + what you want in plain English.
