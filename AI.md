# Hexflow AI Guide

This guide explains how to use the Hexflow framework to create orchestrated workflows from specification files.

## Overview

The Hexflow framework enables AI to:
1. **Parse specification files** describing workflow requirements
2. **Generate DAG files** that define application flow and orchestration
3. **Create modular applications** using skeleton templates
4. **Orchestrate complete workflows** with automatic routing between apps

## Framework Components

### Core Architecture
- **Launcher**: Discovers and starts all applications and the router
- **Router**: Orchestrates workflow navigation based on DAG definitions  
- **Skeletons**: Base templates for creating applications (http_base, casa, display, processor)
- **DAG Files**: YAML workflow definitions that control application flow. They must have the filename extension ".dag"

### Key Directories
- `hexflow/skeletons/` - Application templates
- `examples/` - Example workflows and specifications
- **Application Structure**: Each application must have its own directory containing:
  - `__init__.py` - Package initialization file
  - `app.py` - Main application file with a class inheriting from skeleton templates

## DAG File Format

DAG files are YAML documents that define workflow orchestration:

```yaml
# Workflow metadata
name: "workflow-name"
description: "Brief description of what this workflow does"

# Define applications in the workflow
apps:
  - name: "app-one"           # Must match directory name
    port: 8001                # Unique port for this app
    entry_point: true         # Mark the starting app (only one)
  
  - name: "app-two" 
    port: 8002
    
  - name: "app-three"
    port: 8003

# Define flow between applications  
flow:
  - from: "app-one"
    to: "app-two"
    trigger: "completion"     # Currently only "completion" supported
    # Future: condition: "status == 'success'" for conditional flows
    
  - from: "app-two"  
    to: "app-three"
    trigger: "completion"

# Optional: Data mapping between apps
data_mapping:
  - from: "app-one"
    to: "app-two"
    fields: ["user_input", "session_id"]
    
  - from: "app-two"
    to: "app-three"  
    fields: ["processed_data", "session_id"]

# Runtime configuration
config:
  timeout: 300              # Total workflow timeout in seconds
  retry_attempts: 3         # Retry attempts for failed steps
  parallel_execution: false # Sequential vs parallel execution
```

## Application Creation

### 1. Directory Structure
Each application requires its own directory:
```
project-name/
├── app-one/
│   ├── __init__.py
│   └── app.py
├── app-two/
│   ├── __init__.py  
│   └── app.py
└── workflow.dag
```

### 2. Basic HTTP Application
```python
from hexflow.skeletons.http_base.app import HTTPBaseApp

class AppOne(HTTPBaseApp):
    """Description of what this app does."""
    
    def setup_routes(self):
        """Setup application routes."""
        @self.app.route('/')
        def index():
            return '''
            <h1>App One</h1>
            <p>Application description and interface</p>
            <form action="http://localhost:8000/next" method="get">
                <input type="hidden" name="from" value="app-one">
                <button type="submit">Next →</button>
            </form>
            ''', 200

if __name__ == "__main__":
    app = AppOne(name="app-one", port=8001)
    app.run()
```

### 3. Form-Based Application
```python
from hexflow.skeletons.casa.app import CasaApp

class DataCollector(CasaApp):
    """Form-based data collection application."""
    
    def setup_form(self):
        """Define form fields and validation."""
        return {
            'title': 'Data Collection Form',
            'fields': [
                {
                    'name': 'name',
                    'label': 'Full Name',
                    'type': 'text',
                    'required': True
                },
                {
                    'name': 'email',
                    'label': 'Email Address', 
                    'type': 'email',
                    'required': True
                },
                {
                    'name': 'phone',
                    'label': 'Phone Number',
                    'type': 'tel',
                    'required': True
                }
            ],
            'validation': {
                'email': {
                    'pattern': r'.+@.+\..+',
                    'message': 'Please enter a valid email address'
                }
            }
        }
```

### 4. Custom Application Templates
```python
from hexflow.skeletons.http_base.app import HTTPBaseApp

class CustomTemplate(HTTPBaseApp):
    """Completely custom application template."""
    
    def setup_routes(self):
        """Define custom routes and functionality."""
        @self.app.route('/')
        def index():
            return self.render_custom_interface()
        
        @self.app.route('/api/data')
        def api_endpoint():
            return {'status': 'success', 'data': []}
    
    def render_custom_interface(self):
        """Custom interface rendering logic."""
        return '''
        <h1>Custom Application</h1>
        <p>This template can do anything you need!</p>
        <form action="http://localhost:8000/next" method="get">
            <input type="hidden" name="from" value="custom-app">
            <button type="submit">Next →</button>
        </form>
        '''
```

## Workflow Orchestration

### Flow Control
The router manages application transitions:
- **Entry Point**: `http://localhost:8000/start` redirects to first app
- **Navigation**: Apps redirect to `http://localhost:8000/next?from=app-name`
- **Completion**: Final app completes the workflow

### Session Management
The router maintains workflow state:
- Tracks current application position
- Manages workflow completion status
- Handles data passing between applications (future feature)

### Error Handling
- Invalid DAG files are skipped automatically
- Multiple DAG files: first valid file is used
- Missing applications result in clear error messages

## AI Instructions for DAG Generation

### 1. Analyze Specification Files
When given a specification file:
- Identify discrete processing steps or user interactions
- Determine data flow and dependencies between steps
- Identify entry points and completion criteria

### 2. Map Steps to Applications
For each processing step:
- Create an application directory with unique name
- Assign unique ports starting from 8001
- Determine which skeleton template to use:
  - `http_base`: Basic web applications
  - `casa`: Form-based data collection (future)
  - `processor`: Background processing tasks (future)

### 3. Generate DAG Structure
Create workflow definition:
- Set meaningful workflow name and description
- List all applications with correct ports
- Mark entry point application
- Define sequential or parallel flow between apps
- Add data mapping if applications need to share information

### 4. Create Application Code
For each application:
- Inherit from appropriate skeleton template
- Implement `setup_routes()` method
- Include Next/Complete button that posts to router
- Add appropriate user interface elements
- Handle any business logic specific to that step

## Example: E-commerce Workflow

**Specification**: "Create a workflow for processing orders: collect customer info, validate payment, confirm order"

**Generated DAG**:
```yaml
name: "order-processing"
description: "E-commerce order processing workflow"

apps:
  - name: "customer-info"
    port: 8001
    entry_point: true
    
  - name: "payment-validation"
    port: 8002
    
  - name: "order-confirmation" 
    port: 8003

flow:
  - from: "customer-info"
    to: "payment-validation"
    trigger: "completion"
    
  - from: "payment-validation"
    to: "order-confirmation"
    trigger: "completion"

data_mapping:
  - from: "customer-info"
    to: "payment-validation"
    fields: ["customer_id", "order_details"]
    
  - from: "payment-validation"
    to: "order-confirmation"  
    fields: ["payment_confirmed", "transaction_id"]
```

## Best Practices

### Architecture Principles
- **Router handles ALL state management**: Apps never access databases directly
- **Pluggable backends**: Never hardcode specific backend classes (SQLiteBackend, etc.)
- **Data flows through router**: Apps submit data to router, router manages persistence
- **Apps are stateless**: All persistent state goes through the router's backend system

### Naming Conventions
- Use kebab-case for application names (matches directory names)
- Use descriptive names that reflect application purpose
- Keep DAG names concise but meaningful

### Port Management
- Start application ports at 8001
- Reserve port 8000 for the router
- Assign ports sequentially to avoid conflicts

### Flow Design
- Keep workflows as simple as possible initially
- Use linear flows before adding conditional logic
- Plan for future extensibility with condition fields

### Error Prevention
- Validate all applications exist before generating DAG
- Ensure entry_point is set on exactly one application
- Verify port numbers are unique across all applications
- Never import specific backend classes in applications
- Always route data through the router, never bypass it

## Template System

### Built-in Templates
- **http_base**: Basic HTTP applications with minimal functionality
- **casa**: Form-based applications with validation and styling
- **processor**: Background processing tasks (future)

### Template Flexibility
Templates are designed to be:
- **Subclassable**: Override specific methods while keeping core functionality
- **Replaceable**: Create entirely new templates from scratch
- **Extensible**: Add new methods and functionality as needed

### Casa Form Template Features
The casa template provides:
- **Automatic form rendering** from field configuration
- **Built-in validation** (required fields, patterns, length limits)
- **Multiple field types** (text, email, tel, select, textarea)
- **Error handling** with inline error display
- **Responsive styling** with clean CSS
- **Router integration** with automatic Next buttons

### Local Template Development
Projects can include custom templates in their working directory:

```
project-directory/
├── skeletons/
│   ├── __init__.py
│   └── custom_skeleton.py
├── app-one/
│   └── app.py              # Uses local custom template
├── app-two/
│   └── app.py              # Uses built-in casa template
└── workflow.dag
```

#### Example: Government Digital Service (GDS) Skeletons
The government example demonstrates custom skeletons that inherit from core templates but apply specific styling:

```python
# skeletons/gds_casa.py
from hexflow.skeletons.casa.app import CasaApp

class GDSCasaApp(CasaApp):
    """Government Digital Service form following GDS Design System."""
    
    def __init__(self, name: str = "gds-casa-app", host: str = 'localhost', port: int = 8000):
        super().__init__(name=name, host=host, port=port)
        
    def render_form(self, errors=None):
        """Override to use official GOV.UK Frontend CSS."""
        # Uses official GOV.UK Frontend CSS from CDN
        # <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/govuk-frontend@5.4.1/dist/govuk-frontend.min.css">
        # Authentic Crown logo, GDS colors, proper form components
        return render_template_string(gds_template, ...)
```

**GOV.UK Styling Implementation:**
Both GDS skeletons (casa and display) use local CSS files from the official GOV.UK Frontend:

```python
# Load local GOV.UK CSS in skeleton templates
css_path = os.path.join(os.path.dirname(__file__), 'assets', 'govuk-frontend.min.css')
with open(css_path, 'r', encoding='utf-8') as f:
    govuk_css = f.read()

# Include in template
<style>{{ govuk_css|safe }}</style>
```

**Local CSS Storage:**
- **File location**: `examples/government/skeletons/assets/govuk-frontend.min.css`
- **Source**: Downloaded from official GOV.UK Frontend v5.11.1
- **Size**: 128KB minified CSS with all components and styling

**CSS-Only Benefits:**
- **No JavaScript dependencies**: Lighter weight, faster loading
- **Progressive enhancement**: Works across all browser grades
- **Authentic styling**: Official GOV.UK colors, typography, and layouts
- **Accessibility**: WCAG 2.2 AA compliance built into CSS classes
- **Responsive design**: Mobile-first approach with proper breakpoints
- **Component consistency**: Standardized form elements, buttons, panels
- **Government branding**: Official Crown logo and GOV.UK header styling

**Design System Approach:**
- Uses Block Element Modifier (BEM) naming convention
- CSS classes for styling content instead of global styles
- Components designed to be accessible and responsive without JavaScript
- Maintains consistency with official GOV.UK services

**Using Local Skeletons in Applications:**
```python
# personal-details/app.py
from skeletons.gds_casa import GDSCasaApp

class PersonalDetailsApp(GDSCasaApp):
    def setup_form(self):
        return {
            'title': 'Apply for a library card',
            'fields': [...]
        }
```

**Key Benefits:**
- **Brand consistency**: Apply organization-specific styling across all apps
- **Compliance**: Meet design system requirements (GDS, corporate guidelines)
- **Functionality**: Add specialized validation, integrations, or workflows
- **Reusability**: Share common patterns across multiple workflows

### When to Create Custom Templates
- **Domain-specific functionality**: Specialized business logic
- **Unique UI requirements**: Custom styling or interactions  
- **External integrations**: APIs, databases, services
- **Complex validation**: Business rule validation
- **Performance optimization**: Caching, optimization for specific use cases

## Extending the Framework

### Future Capabilities
- **Conditional flows**: Branch based on application results
- **Parallel execution**: Run multiple applications simultaneously  
- **Data persistence**: Share complex data structures between apps
- **External integrations**: Connect to APIs, databases, etc.
- **Dynamic routing**: Modify workflow based on runtime conditions

### Skeleton Templates
Create new skeleton templates by:
1. Inheriting from `HTTPBaseApp`
2. Adding specialized functionality (forms, APIs, etc.)
3. Providing consistent interfaces for common patterns
4. Including proper Next button integration

This framework provides a foundation for AI to generate sophisticated, orchestrated workflows from high-level specifications while maintaining clean, maintainable code structure.

## Common Issues and Framework Gotchas

### Casa Template Field Configuration

**Issue**: Casa template select fields require `'text'` key, not `'label'`

**Error**: `KeyError: 'text'` when rendering select options

**Solution**: Use this format for select field options:
```python
'options': [
    {'value': 'option1', 'text': 'Display Text 1'},
    {'value': 'option2', 'text': 'Display Text 2'}
]
```

**Wrong**:
```python
'options': [
    {'value': 'option1', 'label': 'Display Text 1'}  # Will cause KeyError
]
```

### F-String CSS Escaping

**Issue**: CSS curly braces in f-strings cause Python parsing errors

**Error**: `NameError: name 'font' is not defined` when CSS contains unescaped braces

**Solution**: Double all curly braces in CSS when using f-strings:
```python
return f'''
<style>
    body {{ font-family: Arial, sans-serif; margin: 0; }}
    .header {{ background-color: #2563eb; }}
</style>
<p>Data: {variable_name}</p>
'''
```

**Wrong**:
```python
return f'''
<style>
    body { font-family: Arial, sans-serif; }  # Will cause NameError
</style>
'''
```

### Data Access in Applications

**Key Pattern**: Applications access workflow data via `request.args`, not direct database calls

**Correct**:
```python
from flask import request

@self.app.route('/')
def index():
    # Get data passed from previous applications
    full_name = request.args.get('full_name', '')
    license_type = request.args.get('license_type', '')
    
    # Use data in response
    return f"Welcome {full_name}, license: {license_type}"
```

**Wrong**:
```python
# Never access backend directly in applications
session = backend.get_session()  # Violates architecture
```

### Wildcard Data Mapping

**For confirmation pages**: Use `"*"` in data_mapping to pass all workflow data:

```yaml
data_mapping:
  - from: "final-form"
    to: "confirmation"
    fields: "*"  # Passes ALL data from entire workflow
```

**For specific data**: List only needed fields:
```yaml
data_mapping:
  - from: "form1"  
    to: "form2"
    fields: ["name", "email"]  # Only passes specific fields
```

### Casa Template Field Types

**Supported field types**:
- `'text'` - Text input
- `'email'` - Email input with validation
- `'tel'` - Telephone input  
- `'date'` - Date picker
- `'select'` - Dropdown with options (requires `'text'` key)
- `'checkbox'` - Single checkbox
- `'textarea'` - Multi-line text

**Checkbox values**: Use `'value'` field for the submitted value when checked:
```python
{
    'name': 'terms_accepted',
    'type': 'checkbox', 
    'value': 'accepted',  # This gets submitted when checked
    'required': True
}
```

### Import Requirements

**Applications need Flask request**:
```python
from flask import request  # Required for accessing workflow data
```

**Random data generation**:
```python
import random  # For generating reference numbers, etc.
```

### DAG File Common Mistakes

**Entry point**: Exactly one app must have `entry_point: true`
```yaml
apps:
  - name: "first-app"
    port: 8001
    entry_point: true  # Only one app can have this
  - name: "second-app" 
    port: 8002
    # No entry_point field for subsequent apps
```

**Port conflicts**: Each app needs unique port starting from 8001 (router uses 8000)
**Flow definition**: Every app except the last should have a flow definition
**Data mapping**: Must match actual form field names from previous steps

### Validation Patterns

**UK Postcode validation**:
```python
'validation': {
    'postcode': {
        'pattern': r'^[A-Z]{1,2}[0-9][A-Z0-9]?\s?[0-9][A-Z]{2}$',
        'message': 'Please enter a valid UK postcode'
    }
}
```

**Required field validation**:
```python
'validation': {
    'field_name': {
        'required': True,
        'message': 'This field is required'
    }
}
```

### Directory Structure Requirements

**Each application must have**:
```
app-name/
├── __init__.py     # Required (can be empty)
└── app.py          # Must contain the application class
```

**Class naming**: Class name should match purpose, not directory name:
```python
# In directory "name-and-address/app.py"
class NameAndAddressApp(CasaApp):  # Descriptive class name
    pass
```

### Constructor Patterns

**Skeleton app constructors must accept launcher parameters**:

```python
# CasaApp and DisplayApp constructors - CORRECT
class MyFormApp(CasaApp):
    def __init__(self, name="my-form", host='localhost', port=8001):
        super().__init__(name=name, host=host, port=port)

class MyDisplayApp(DisplayApp):  
    def __init__(self, name="my-display", host='localhost', port=8002):
        super().__init__(name=name, host=host, port=port)
```

**Wrong** - Constructor doesn't accept launcher parameters:
```python
class MyFormApp(CasaApp):
    def __init__(self):  # Missing name, host, port parameters
        super().__init__(name="my-form", host='localhost', port=8001)
    # Error: "unexpected keyword argument 'name'" when launcher tries to instantiate
```

**Wrong** - Missing parameters causes misleading error messages:
```python
def __init__(self, name="my-app", port=8001):  # Missing 'host' parameter
    super().__init__(name=name, port=port)
    # Error: "unexpected keyword argument 'name'"
```

**Correct** - Accept and pass through all launcher parameters:
```python
def __init__(self, name="my-app", host='localhost', port=8001):
    super().__init__(name=name, host=host, port=port)
```

**Why**: The launcher calls `app_class(name=app_name, port=port)`, so your constructor must accept these parameters.

### Architecture Violations to Avoid

1. **Never import backend classes** in applications
2. **Never access databases directly** from applications  
3. **Never hardcode data** - always use workflow data from router
4. **Never bypass router** for data passing between applications
5. **Never create stateful applications** - state belongs in router backend

These patterns ensure applications remain pluggable, testable, and follow the framework's data flow architecture.

## Automated Test Generation

### Test Generation from Specifications

When creating workflows from specification files, automatically generate Playwright end-to-end tests to validate the workflow behavior. This ensures comprehensive testing coverage and maintains quality as specifications evolve.

### Test Structure Pattern

For each workflow specification, create tests **within the workflow directory**, following this pattern:

```
examples/workflow-name/
├── apps/                          # Workflow applications
├── skeletons/                     # Local templates (if any)
├── tests/                         # Tests belong WITH the workflow
│   ├── __init__.py
│   ├── conftest.py               # Workflow-specific fixtures
│   └── test_workflow_name.py     # Main test file
├── playwright.config.py          # Playwright config for this workflow
├── pytest.ini                    # Pytest config for this workflow
├── requirements-test.txt          # Test dependencies for this workflow
├── run_tests.py                   # Test runner script
├── workflow.dag                   # Workflow definition
└── *.spec.*                      # Specification files
```

**CRITICAL**: Tests belong with the workflow, NOT in the framework. Each workflow has its own isolated test suite.

### Test Generation Steps

1. **Parse Specification Scenarios**: Extract test scenarios from `.spec.feature` or `.spec.yaml` files
2. **Generate Test Methods**: Create one test method per scenario
3. **Create Helper Methods**: Generate common form-filling utilities
4. **Add Field Validation Tests**: Test that all fields are visible and functional
5. **Include Error Validation**: Test validation rules and error messages

### Example Test Generation

**From Specification**:
```gherkin
@app(id="personal-details", skeleton="casa", port=8001, entry_point=true)
Scenario: Submit personal details successfully
  Given the form "personal-details" has fields:
    | name      | label        | type  | required |
    | full_name | Full name    | text  | true     |
    | email     | Email address| email | true     |
  When the user submits valid personal details
  Then route to "library-preferences"
```

**Generated Test**:
```python
def test_personal_details_valid_submission(self, page: Page, workflow_url: str):
    """Test successful submission of personal details form."""
    page.goto(workflow_url)
    
    # Verify form is rendered
    expect(page.locator("h1")).to_contain_text("personal details")
    
    # Fill valid data
    page.fill("input[name='full_name']", "John Smith")
    page.fill("input[name='email']", "john.smith@example.com")
    
    # Submit form
    page.click("button[type='submit']")
    
    # Verify navigation to next step
    expect(page.locator("h1")).to_contain_text("library preferences")
```

### Test Categories to Generate

#### 1. Happy Path Tests
- **Complete workflow**: Test full successful flow from start to finish
- **Data persistence**: Verify data carries between steps correctly
- **Field visibility**: Ensure all specified fields are present and functional

#### 2. Validation Tests
- **Required fields**: Test missing required field validation
- **Pattern validation**: Test regex patterns (postcodes, emails, phone numbers)
- **Custom validation**: Test business rule validation
- **Error messages**: Verify correct error messages are displayed

#### 3. Navigation Tests
- **Step transitions**: Test navigation between workflow steps
- **Entry point**: Verify workflow starts at correct app
- **Completion**: Test successful workflow completion

#### 4. UI Tests
- **Form rendering**: Test that forms render with correct fields and labels
- **Responsive design**: Test on different viewport sizes
- **Accessibility**: Test keyboard navigation and screen reader compatibility

### Fixture Pattern for Workflow Management

```python
@pytest.fixture(scope="session")
def workflow_runner():
    """Fixture to manage workflow lifecycle during tests."""
    # Import framework from parent directories
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    
    from hexflow.launcher.app_launcher import AppLauncher
    
    # Workflow path is the parent directory of tests/
    workflow_path = Path(__file__).parent.parent
    launcher = AppLauncher(str(workflow_path))
    
    try:
        launcher.launch_all_apps()
        # Wait for services to be ready
        yield launcher
    finally:
        launcher.stop_all_apps()
```

### Helper Method Patterns

Generate helper methods for common operations:

```python
def _fill_valid_personal_details(self, page: Page, name="John Smith", email="john.smith@example.com"):
    """Fill personal details form with valid data."""
    page.fill("input[name='full_name']", name)
    page.fill("input[name='email']", email)
    # ... other fields

def _expect_validation_error(self, page: Page, field_name: str, error_text: str):
    """Verify validation error is displayed for a field."""
    error_selector = f".govuk-error-message, .error"  # Support multiple CSS frameworks
    expect(page.locator(error_selector)).to_contain_text(error_text)
```

### Test Configuration

**Playwright Configuration**:
```python
config = {
    "testDir": "./tests/e2e",
    "timeout": 30000,
    "fullyParallel": False,  # Workflows share ports
    "workers": 1,  # Avoid port conflicts
    "use": {
        "baseURL": "http://localhost:8000",
        "trace": "on-first-retry",
        "screenshot": "only-on-failure",
    }
}
```

### Integration with Specification Changes

When specifications change:
1. **Regenerate tests**: Update test file to match new scenarios
2. **Update fixtures**: Modify workflow path if directory structure changes
3. **Validate coverage**: Ensure all scenarios have corresponding tests
4. **Run regression tests**: Verify existing functionality still works

### Test Naming Conventions

- Test files: `test_{workflow_name}_workflow.py`
- Test methods: `test_{scenario_name}_{condition}`
- Helper methods: `_action_description`
- Fixtures: `{workflow_name}_workflow`

### Benefits of Automated Test Generation

1. **Comprehensive Coverage**: Every specification scenario gets a test
2. **Consistency**: Standardized test patterns across all workflows
3. **Maintenance**: Tests stay synchronized with specifications
4. **Quality Assurance**: Catch regressions during workflow evolution
5. **Documentation**: Tests serve as executable specifications

### Test Execution

**Run workflow tests** (from within workflow directory):
```bash
cd examples/government
python run_tests.py
```

**Or run with pytest directly**:
```bash
cd examples/government  
pytest tests/ -v
```

**Generate test report**:
```bash
pytest tests/ --html=test-report.html
```

This pattern ensures that every workflow specification automatically gets comprehensive test coverage, maintaining quality and catching regressions as workflows evolve.