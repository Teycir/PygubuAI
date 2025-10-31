# Running PygubuAI Examples

Quick guide to run all example applications.

## Prerequisites

Install pygubu:

```bash
pip install pygubu
```

Or if you get an externally-managed-environment error:

```bash
pip install --break-system-packages pygubu
```

## Run All Examples

### 1. Calculator

```bash
cd examples/calculator
python3 calculator.py
```

Features: Number pad, operations, clear, backspace

### 2. Todo App

```bash
cd examples/todo_app
python3 todo_app.py
```

Features: Add tasks, delete, clear all, task counter

### 3. Login Form

```bash
cd examples/login_form
python3 login_form.py
```

Features: Username/password, validation, remember me
Test credentials: admin/password

### 4. Settings Dialog

```bash
cd examples/settings_dialog
python3 settings_dialog.py
```

Features: Tabbed interface, checkboxes, dropdown, slider

### 5. Data Viewer

```bash
cd examples/data_viewer
python3 data_viewer.py
```

Features: Table view, search, load/refresh data

### 6. Number Game

```bash
cd examples/number_game
python3 number_game.py
```

Features: Guess number 1-100, feedback, attempts counter

## Run from Root Directory

```bash
# From PygubuAI root
python3 examples/calculator/calculator.py
python3 examples/todo_app/todo_app.py
python3 examples/login_form/login_form.py
python3 examples/settings_dialog/settings_dialog.py
python3 examples/data_viewer/data_viewer.py
python3 examples/number_game/number_game.py
```

## Troubleshooting

### No module named 'pygubu'

Install pygubu:
```bash
pip install pygubu
```

### Display issues

Ensure you have a graphical environment (X11, Wayland, etc.)

### Permission denied

Make files executable:
```bash
chmod +x examples/*/*.py
```

## Quick Test All

```bash
cd examples
for app in calculator todo_app login_form settings_dialog data_viewer number_game; do
    echo "Testing $app..."
    python3 $app/$app.py &
    sleep 1
    pkill -f $app.py
done
echo "All examples tested"
```
