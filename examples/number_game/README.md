# Number Guessing Game Example

A simple number guessing game demonstrating PygubuAI workflow integration.

## Running the Example

```bash
cd examples/number_game
python number_game.py
```

## Game Rules

- Guess a number between 1 and 100
- Get feedback if your guess is too high or low
- Track your attempts
- Reset to play again

## PygubuAI Workflow

Edit the UI visually and sync with code:

```bash
# Edit UI in designer
pygubu-designer number_game.ui

# Watch for changes (in another terminal)
pygubu-ai-workflow watch number_game

# Ask AI to sync code after UI changes
```

## Features Demonstrated

- Entry widget with validation
- Button callbacks
- Label updates
- State management (enable/disable widgets)
- Keyboard bindings (Enter key)
