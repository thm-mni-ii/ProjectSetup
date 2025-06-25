# ProjectSetup

This repository provides a template for setting up a project with two Databases: PostgreSQL and MongoDB, along with a Python backend and a Vue.js frontend. It includes Docker configurations for easy deployment and management.

## Requirements
- Visual Studio Code
    - Recommended Extensions
        - Database Client
        - Docker
        - ESLint
        - Prettier
        - Path Intellisense
        - Python
        - Pylint
        - Vite
        - Vue - Official
- Python 3.10 or higher
- Git (for version control)
- Docker
- Node.js v22.12.0 (for the Vue.js frontend)
- Node Version Manager (nvm) (optional, for managing Node.js versions)
- conda (optional, for managing Python environments)

### Recommended VS Code Settings
Open the settings.json file in VS Code and add the following configurations. You can access this file by clicking on the gear icon in the lower left corner, selecting "Settings", and then clicking on the "Open Settings (JSON)" icon in the top right corner.

Insert the following JSON configuration into your `settings.json` file. If the file already contains some settings, you can merge them with the existing ones.

```json
{
"[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  },
  "[vue]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[jsonl]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "editor.inlineSuggest.enabled": true,
  "eslint.codeActionsOnSave.rules": null,
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[python]": {
    "editor.formatOnType": true
  },
  "files.autoSave": "afterDelay",
  "[jsonc]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[html]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "typescript.updateImportsOnFileMove.enabled": "always",
}
```

### Recommended when using conda
If you are using conda for managing your Python environments, you can use the following command to create a new environment with Python 3.10:

```bash
conda create -n project_env python=3.10
```
Activate the environment with:

```bash
conda activate project_env
```

After creating and activating the environment, you can install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

Finally, change the Python interpreter in VS Code to use the conda environment. You can do this by opening the command palette (Ctrl+Shift+P), typing "Python: Select Interpreter", and selecting the interpreter from your conda environment.

