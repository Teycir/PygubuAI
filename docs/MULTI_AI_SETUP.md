# PygubuAI Multi-AI Setup Guide

PygubuAI now supports multiple AI coding assistants. Just say "pygubuai" in any of these tools!

## Supported AI Assistants

- Amazon Q Developer
- Kilo Code
- Roo Code
- Cline

## Quick Setup

### One-Time Setup (All Tools)

```bash
cd /home/teycir/Repos/PygubuAI

# For Amazon Q
bash scripts/setup-amazonq.sh scan ~/Repos

# For Kilo Code
bash scripts/setup-kilocode.sh scan ~/Repos

# For Roo Code
bash scripts/setup-roocode.sh scan ~/Repos

# For Cline
bash scripts/setup-cline.sh scan ~/Repos
```

### Mark Single Project

```bash
# Amazon Q
bash scripts/setup-amazonq.sh mark /path/to/project

# Kilo Code
bash scripts/setup-kilocode.sh mark /path/to/project

# Roo Code
bash scripts/setup-roocode.sh mark /path/to/project

# Cline
bash scripts/setup-cline.sh mark /path/to/project
```

### Mark PygubuAI Repo Only

```bash
bash scripts/setup-amazonq.sh self      # Amazon Q
bash scripts/setup-kilocode.sh self     # Kilo Code
bash scripts/setup-roocode.sh self      # Roo Code
bash scripts/setup-cline.sh self        # Cline
```

## Configuration Directories

Each AI tool has its own configuration:

```
PygubuAI/
├── .amazonq/
│   ├── prompts/pygubu-context.md
│   └── rules/pygubuai-trigger.md
├── .kilocode/
│   ├── prompts/pygubu-context.md
│   └── rules/pygubuai-trigger.md
├── .roocode/
│   ├── prompts/pygubu-context.md
│   └── rules/pygubuai-trigger.md
└── .cline/
    ├── prompts/pygubu-context.md
    └── rules/pygubuai-trigger.md
```

## Usage

After setup, just say "pygubuai" in any AI assistant:

```
pygubuai create a login form
pygubuai add a submit button
pygubuai show my projects
pygubuai build a dashboard
```

Works the same across all AI tools!

## How It Works

1. Setup script creates `.pygubuai` marker files in project directories
2. AI tools detect the marker and load PygubuAI context
3. Natural language commands are automatically translated to pygubu operations
4. No need to remember command syntax

## Verification

Check if setup worked:

```bash
# Find all marked projects
find ~/Repos -name ".pygubuai" -type f

# Should show directories with .pygubuai marker files
```

## Troubleshooting

If "pygubuai" keyword doesn't work:

1. Verify marker file exists: `ls -la .pygubuai`
2. Check configuration directory exists for your AI tool
3. Restart your IDE/editor
4. Re-run setup script

## Notes

- All AI tools share the same `.pygubuai` marker files
- Each tool has separate configuration directories
- Setup is non-destructive and can be run multiple times
- Works from any subdirectory of a marked project
