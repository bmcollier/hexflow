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

2. **Write a specification file** (`my-workflow.spec.md`):
```markdown
# My Workflow Specification
# See https://github.com/bmcollier/hexflow/blob/main/AI.md to understand how to use this

## Overview
A simple workflow that collects a user's name and displays a greeting.

## Steps
1. **Step One**: Collect user's name via form
2. **Step Two**: Display personalized greeting

## Fields
- name: User's full name (required)
```

3. **Optionally add structured specifications**:
- `my-workflow.spec.yaml`: YAML structure for forms and validation
- `my-workflow.spec.feature`: Gherkin scenarios for testing

4. **Instruct AI to generate the workflow**:
```
Please read AI.md and generate the complete workflow applications based on my-workflow.spec.md
```

5. **Launch the generated workflow**:
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