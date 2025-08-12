# Hexflow

AI-aware modular application framework for creating orchestrated workflows.

## Overview

Hexflow is a Python framework that enables AI to automatically generate complex, multi-step workflows from natural language specifications. It provides a modular architecture where individual applications handle specific tasks, and an intelligent router orchestrates the flow between them.

## Key Features

- **AI-Driven**: Designed for AI agents to generate workflows from specifications
- **Modular Architecture**: Each step is an independent application
- **Form-Based Applications**: Built-in support for data collection forms
- **Workflow Orchestration**: Automatic routing and data passing between applications
- **Persistent State**: Sessions survive page reloads and continue across devices
- **Template System**: Extensible skeleton system for rapid development
- **Local Customization**: Override templates for organization-specific styling

## Quick Start

### Installation

```bash
pip install hexflow
```

### Create Your First Workflow

1. **Create a workflow directory**:
```bash
mkdir my-workflow
cd my-workflow
```

2. **Define the workflow in a DAG file** (`workflow.dag`):
```yaml
name: "simple-workflow"
description: "A simple two-step workflow"

apps:
  - name: "step-one"
    port: 8001
    entry_point: true
    
  - name: "step-two"
    port: 8002

flow:
  - from: "step-one"
    to: "step-two"
    trigger: "completion"
```

3. **Create applications** in subdirectories:

`step-one/app.py`:
```python
from hexflow.skeletons.casa.app import CasaApp

class StepOneApp(CasaApp):
    def setup_form(self):
        return {
            'title': 'Step One',
            'fields': [
                {
                    'name': 'name',
                    'label': 'Your Name',
                    'type': 'text',
                    'required': True
                }
            ]
        }
```

`step-two/app.py`:
```python
from hexflow.skeletons.http_base.app import HTTPBaseApp
from flask import request

class StepTwoApp(HTTPBaseApp):
    def setup_routes(self):
        @self.app.route('/')
        def index():
            name = request.args.get('name', 'Anonymous')
            return f"<h1>Hello {name}!</h1><p>Workflow completed.</p>"
```

4. **Add `__init__.py` files**:
```bash
touch step-one/__init__.py step-two/__init__.py
```

5. **Launch the workflow**:
```bash
hexflow .
```

Visit `http://localhost:8000/start` to begin your workflow.

## Architecture

### Core Components

- **Launcher**: Discovers and starts all applications
- **Router**: Orchestrates navigation between applications based on DAG definitions
- **Skeletons**: Base templates for different types of applications
- **State Backend**: Manages persistent session data

### Application Types

- **Casa Apps**: Form-based applications with validation
- **Display Apps**: Read-only confirmation and summary pages
- **HTTP Base Apps**: Fully customizable applications
- **Processor Apps**: Background processing tasks (future)

## Examples

The framework includes several complete examples:

- **Self-Test**: Simple three-step workflow demonstrating basic concepts
- **Fishing License**: Government service application with forms and validation
- **Employee Onboarding**: Multi-step HR process with data collection

Run examples:
```bash
git clone https://github.com/bmcollier/hexflow
cd hexflow/examples/fishing
hexflow .
```

## Documentation

For detailed documentation, including:
- Complete API reference
- Advanced workflow patterns
- Custom skeleton development
- Testing strategies

See [AI.md](https://github.com/bmcollier/hexflow/blob/main/AI.md)

## Contributing

We welcome contributions! Please see our contributing guidelines and submit issues or pull requests on GitHub.

## License

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Links

- **Source Code**: https://github.com/bmcollier/hexflow
- **Bug Reports**: https://github.com/bmcollier/hexflow/issues
- **PyPI Package**: https://pypi.org/project/hexflow/