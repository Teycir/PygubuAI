# Installation Guide

## Prerequisites

- Python 3.9 or higher
- pip package manager
- tkinter (usually included with Python)

## Step 1: Install Pygubu

```bash
pip install pygubu pygubu-designer
```

Verify installation:
```bash
python -c "import pygubu; print(pygubu.__version__)"
```

## Step 2: Install PygubuAI

### Option A: Quick Install (Recommended)

```bash
git clone https://github.com/yourusername/pygubuai.git
cd pygubuai
./install.sh
```

### Option B: Manual Install

```bash
git clone https://github.com/yourusername/pygubuai.git
cd pygubuai

# Copy tools to ~/bin
mkdir -p ~/bin
cp pygubu-* ~/bin/
cp tkinter-to-pygubu ~/bin/
chmod +x ~/bin/pygubu-* ~/bin/tkinter-to-pygubu

# Add to PATH
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## Step 3: Verify Installation

```bash
pygubu-create --help
pygubu-register list
```

## Troubleshooting

### Command not found
Ensure `~/bin` is in your PATH:
```bash
echo $PATH | grep "$HOME/bin"
```

### Missing pygubu
```bash
pip install --upgrade pygubu pygubu-designer
```

### Permission denied
```bash
chmod +x ~/bin/pygubu-*
```
