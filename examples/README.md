# PygubuAI Examples

Complete working examples demonstrating PygubuAI features and workflows.

## Available Examples

### 1. Number Guessing Game
**Path:** `number_game/`
**Difficulty:** Beginner

A simple game demonstrating basic widgets and callbacks.

Features:
- Entry validation
- Button callbacks
- Label updates
- State management

```bash
cd number_game && python number_game.py
```

### 2. Todo List Application
**Path:** `todo_app/`
**Difficulty:** Beginner

A complete task manager with add, delete, and clear functions.

Features:
- Listbox with scrollbar
- Dynamic updates
- Task counter
- Keyboard shortcuts

```bash
cd todo_app && python todo_app.py
```

### 3. Calculator
**Path:** `calculator/`
**Difficulty:** Intermediate

A functional calculator with number pad and operations.

Features:
- Grid layout
- Multiple button callbacks
- Operation handling
- Error handling

```bash
cd calculator && python calculator.py
```

### 4. Login Form
**Path:** `login_form/`
**Difficulty:** Beginner

A professional login interface with validation.

Features:
- Password masking
- Form validation
- Checkbutton widget
- Visual feedback

```bash
cd login_form && python login_form.py
```

### 5. Settings Dialog
**Path:** `settings_dialog/`
**Difficulty:** Intermediate

A tabbed settings interface with various input types.

Features:
- Notebook (tabs) widget
- Checkbuttons
- Combobox
- Scale widget

```bash
cd settings_dialog && python settings_dialog.py
```

### 6. Data Viewer
**Path:** `data_viewer/`
**Difficulty:** Advanced

A data table viewer with search and filtering.

Features:
- Treeview with columns
- Search functionality
- Toolbar
- Status bar

```bash
cd data_viewer && python data_viewer.py
```

## Running Examples

### Prerequisites

Install pygubu:
```bash
pip install pygubu
```

### Quick Run

From project root:
```bash
./run_example.sh calculator
./run_example.sh todo_app
./run_example.sh login_form
./run_example.sh settings_dialog
./run_example.sh data_viewer
./run_example.sh number_game
```

### Manual Run

```bash
cd examples/calculator
python3 calculator.py
```

See [RUN_EXAMPLES.md](RUN_EXAMPLES.md) for detailed instructions.

## Learning Path

1. Start with **number_game** - Learn basic widgets
2. Try **todo_app** - Understand lists and dynamic updates
3. Build **login_form** - Master form validation
4. Explore **calculator** - Work with grid layouts
5. Study **settings_dialog** - Use advanced widgets
6. Analyze **data_viewer** - Handle complex data

## Creating Your Own

Use these examples as templates:

```bash
# Copy an example
cp -r examples/todo_app my_project

# Or create from scratch
pygubu-create myapp 'description of your app'

# Or use a template
pygubu-template myapp login
```

## Modifying Examples

Each example can be edited visually:

```bash
cd examples/todo_app
pygubu-designer todo_app.ui
```

Then ask AI to sync the code:
- "I added a priority dropdown, update the code"
- "Add save to file functionality"
- "Change the color scheme"

## Widget Showcase

Examples demonstrate these widgets:

- **Entry** - Text input (all examples)
- **Button** - Actions (all examples)
- **Label** - Display text (all examples)
- **Listbox** - Lists (todo_app)
- **Treeview** - Tables (data_viewer)
- **Checkbutton** - Boolean options (login_form, settings_dialog)
- **Combobox** - Dropdowns (settings_dialog)
- **Scale** - Sliders (settings_dialog)
- **Notebook** - Tabs (settings_dialog)
- **Scrollbar** - Scrolling (todo_app, data_viewer)

## PygubuAI Features Demonstrated

- Natural language creation
- Template-based generation
- Visual-to-code workflow
- AI-assisted enhancement
- Project registry integration
- Watch mode for live updates

## Contributing Examples

Have a great example? Submit a PR:

1. Create folder in `examples/`
2. Include `.ui`, `.py`, and `README.md`
3. Follow existing structure
4. Add to this README

## Support

Questions about examples? Check:
- Individual example READMEs
- [User Guide](../docs/USER_GUIDE.md)
- [Onboarding](../docs/ONBOARDING.md)
- [GitHub Issues](https://github.com/Teycir/PygubuAI/issues)
