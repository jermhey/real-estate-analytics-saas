# VS Code Settings for Real Estate Analytics SaaS

To fix red filenames and import warnings in VS Code:

## 1. Set Python Interpreter
1. Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux)
2. Type "Python: Select Interpreter"
3. Choose: `./venv/bin/python` (the virtual environment Python)

## 2. VS Code Settings (.vscode/settings.json)
```json
{
    "python.pythonPath": "./venv/bin/python",
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.analysis.extraPaths": ["./app"],
    "python.analysis.autoImportCompletions": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black"
}
```

## 3. Install Type Stubs (Optional)
```bash
cd "/Users/jeremy/Desktop/DSCI 112 Project/real_estate_saas"
source venv/bin/activate
pip install types-requests types-flask types-sqlalchemy
```

This will eliminate most red filename warnings while keeping full functionality.
