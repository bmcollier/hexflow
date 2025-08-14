"""GDS Display application skeleton following UK Government Design System guidelines."""

import sys
import os
from flask import request, render_template_string, render_template
from markupsafe import Markup
from typing import Dict, List, Any, Optional

# Add the parent directory to the path so we can import hexflow
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from hexflow.skeletons.display.app import DisplayApp


class GDSDisplayApp(DisplayApp):
    """Government Digital Service display application following GDS Design System."""
    
    def __init__(self, name: str = "gds-display-app", host: str = 'localhost', port: int = 8000, service_name: str = None):
        super().__init__(name=name, host=host, port=port)
        
        # Set service name - default to a generic name if not provided
        self.service_name = service_name or "Government Service"
        
        # Set up template folder for Jinja2
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        if os.path.exists(template_dir):
            self.app.template_folder = template_dir
        
        # Set up static asset serving
        self.setup_static_assets()
    
    def setup_static_assets(self):
        """Set up routes to serve GOV.UK assets with proper MIME types."""
        from flask import send_from_directory, make_response
        import mimetypes
        
        assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
        
        # Register font MIME types
        mimetypes.add_type('font/woff2', '.woff2')
        mimetypes.add_type('font/woff', '.woff')
        mimetypes.add_type('application/font-woff2', '.woff2')
        mimetypes.add_type('application/font-woff', '.woff')
        
        @self.app.route('/assets/<path:filename>')
        def serve_display_assets(filename):
            return self._serve_asset_file(assets_dir, filename)
        
        @self.app.route('/stylesheets/<filename>')
        def serve_stylesheets(filename):
            return self._serve_asset_file(assets_dir, filename)
        
        @self.app.route('/javascripts/<filename>')
        def serve_javascripts(filename):
            # JavaScript file doesn't exist, return 404 with proper MIME type
            from flask import abort
            abort(404)
        
        @self.app.route('/assets/rebrand/<path:filename>')
        def serve_rebrand_assets(filename):
            # Rebrand assets don't exist, return 404 gracefully
            from flask import abort
            abort(404)
    
    def _serve_asset_file(self, assets_dir, filename):
        """Helper method to serve asset files with proper MIME types."""
        from flask import send_from_directory, make_response
        
        try:
            response = make_response(send_from_directory(assets_dir, filename))
            
            # Set proper MIME types
            if filename.endswith('.woff2'):
                response.headers['Content-Type'] = 'font/woff2'
                response.headers['Access-Control-Allow-Origin'] = '*'
            elif filename.endswith('.woff'):
                response.headers['Content-Type'] = 'font/woff'
                response.headers['Access-Control-Allow-Origin'] = '*'
            elif filename.endswith('.css'):
                response.headers['Content-Type'] = 'text/css'
            elif filename.endswith('.js'):
                response.headers['Content-Type'] = 'application/javascript'
            elif filename.endswith('.png'):
                response.headers['Content-Type'] = 'image/png'
            elif filename.endswith('.svg'):
                response.headers['Content-Type'] = 'image/svg+xml'
            elif filename.endswith('.ico'):
                response.headers['Content-Type'] = 'image/x-icon'
            
            return response
        except Exception as e:
            print(f"ERROR serving {filename}: {e}")
            raise
    
    def setup_routes(self):
        """Setup display routes using GDS styling."""
        
        @self.app.route('/', methods=['GET', 'POST'])
        def display_handler():
            # Get workflow data from form data (POST) or URL parameters (GET)
            if request.method == 'POST':
                # Process form data properly - request.form is a MultiDict
                workflow_data = {}
                for key, value in request.form.items():
                    workflow_data[key] = value
            else:
                workflow_data = dict(request.args)
            
            workflow_token = workflow_data.pop('workflow_token', '')
            print(f"DEBUG: Workflow data received: {workflow_data}")
            
            # Call setup_display with workflow data
            self.display_config = self.setup_display(workflow_data)
            
            # Use our custom GDS render method
            return self.render_display(workflow_data)
        
    def render_display(self, workflow_data=None) -> str:
        """Render the display HTML using GDS Design System styling."""
        display_config = self.display_config
        workflow_data = workflow_data or {}
        
        # Build sections HTML
        sections_html = []
        for section in display_config.get('sections', []):
            section_html = self.render_gds_section(section)
            sections_html.append(section_html)
        
        # Get workflow data if requested
        workflow_data_html = ''
        if display_config.get('show_workflow_data', False):
            workflow_data_html = self.render_workflow_data(workflow_data)
        
        # GDS-compliant template with 2025 rebrand
        template = '''
        <!DOCTYPE html>
        <html lang="en" class="govuk-template govuk-template--rebranded">
        <head>
            <meta charset="utf-8">
            <title>{{ title }} - GOV.UK</title>
            <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
            <meta name="theme-color" content="#0b0c0c">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            
            <!-- GOV.UK Frontend CSS (Local) -->
            <style>
                /* Load local GOV.UK Frontend CSS */
                {{ govuk_css|safe }}
            </style>
            
            <style>
                /* Minor customizations for enhanced display */
                .govuk-form-group {
                    margin-bottom: 20px;
                }
            </style>
        </head>
        <body class="govuk-template__body">
            <script>
                document.body.className += ' js-enabled' + ('noModule' in HTMLScriptElement.prototype ? ' govuk-frontend-supported' : '');
            </script>
            
            <a href="#main-content" class="govuk-skip-link" data-module="govuk-skip-link">Skip to main content</a>
            <header class="govuk-header" data-module="govuk-header">
                <div class="govuk-header__container govuk-width-container">
                    <div class="govuk-header__logotype">
                        <a href="https://www.gov.uk/" class="govuk-header__link govuk-header__link--homepage">
                            <span class="govuk-header__logotype">
                                <svg
                                    aria-hidden="true"
                                    focusable="false"
                                    class="govuk-header__logotype-crown"
                                    xmlns="http://www.w3.org/2000/svg"
                                    viewBox="0 0 32 30"
                                    height="30"
                                    width="32"
                                >
                                    <path
                                        fill="currentColor" fill-rule="evenodd"
                                        d="M22.6 10.4c-1 .4-2-.1-2.4-1-.4-.9.1-2 1-2.4.9-.4 2 .1 2.4 1s-.1 2-1 2.4m-5.9 6.7c-.9.4-2-.1-2.4-1-.4-.9.1-2 1-2.4.9-.4 2 .1 2.4 1s-.1 2-1 2.4m2.8-9.1c-.9.4-2-.1-2.4-1-.4-.9.1-2 1-2.4.9-.4 2 .1 2.4 1s0 2-1 2.4m0 8.6c-.9.4-2-.1-2.4-1-.4-.9.1-2 1-2.4.9-.4 2 .1 2.4 1s-.1 2-1 2.4m-2.1-7.1c-.9.4-2-.1-2.4-1-.4-.9.1-2 1-2.4.9-.4 2 .1 2.4 1s-.1 2-1 2.4m-2.3 5.6c-.9.4-2-.1-2.4-1-.4-.9.1-2 1-2.4.9-.4 2 .1 2.4 1s-.1 2-1 2.4m1.6 1.9c-.9.4-2-.1-2.4-1-.4-.9.1-2 1-2.4.9-.4 2 .1 2.4 1s-.1 2-1 2.4m0-4.4c-.9.4-2-.1-2.4-1-.4-.9.1-2 1-2.4.9-.4 2 .1 2.4 1s-.1 2-1 2.4m2.3-1.6c-.9.4-2-.1-2.4-1-.4-.9.1-2 1-2.4.9-.4 2 .1 2.4 1s-.1 2-1 2.4M7.7 21c.9.4 2-.1 2.4-1 .4-.9-.1-2-1-2.4-.9-.4-2 .1-2.4 1s.1 2 1 2.4m-5.5-6.9c.9.4 2-.1 2.4-1 .4-.9-.1-2-1-2.4-.9-.4-2 .1-2.4 1s.1 2 1 2.4m2.8 9.2c.9.4 2-.1 2.4-1 .4-.9-.1-2-1-2.4-.9-.4-2 .1-2.4 1s.1 2 1 2.4m0-8.6c.9.4 2-.1 2.4-1 .4-.9-.1-2-1-2.4-.9-.4-2 .1-2.4 1s.1 2 1 2.4m2.1 7.1c.9.4 2-.1 2.4-1 .4-.9-.1-2-1-2.4-.9-.4-2 .1-2.4 1s.1 2 1 2.4m2.3-5.6c.9.4 2-.1 2.4-1 .4-.9-.1-2-1-2.4-.9-.4-2 .1-2.4 1s.1 2 1 2.4m-1.6-1.9c.9.4 2-.1 2.4-1 .4-.9-.1-2-1-2.4-.9-.4-2 .1-2.4 1s.1 2 1 2.4m0 4.4c.9.4 2-.1 2.4-1 .4-.9-.1-2-1-2.4-.9-.4-2 .1-2.4 1s.1 2 1 2.4m-2.3 1.6c.9.4 2-.1 2.4-1 .4-.9-.1-2-1-2.4-.9-.4-2 .1-2.4 1s.1 2 1 2.4"
                                    />
                                </svg>
                                <span class="govuk-header__logotype-text">
                                    GOV.UK
                                </span>
                            </span>
                        </a>
                    </div>
                    <div class="govuk-header__content">
                        <span class="govuk-header__product-name">{{ service_name }}</span>
                    </div>
                </div>
            </header>
            
            <div class="govuk-width-container">
                <main class="govuk-main-wrapper" id="main-content" role="main">
                    <div class="govuk-grid-row">
                        <div class="govuk-grid-column-two-thirds">
                            <div class="govuk-panel govuk-panel--confirmation">
                                <h1 class="govuk-panel__title">{{ title }}</h1>
                            </div>
                            
                            {{ sections_html|safe }}
                            {{ workflow_data_html|safe }}
                            
                            <div class="govuk-inset-text">
                                {{ completion_message }}
                            </div>
                        </div>
                    </div>
                </main>
            </div>
            
            <!-- GOV.UK Frontend JavaScript would go here if available -->
        </body>
        </html>
        '''
        
        # Load GOV.UK Frontend CSS
        css_path = os.path.join(os.path.dirname(__file__), 'assets', 'govuk-frontend.min.css')
        try:
            with open(css_path, 'r', encoding='utf-8') as f:
                govuk_css = f.read()
        except FileNotFoundError:
            print(f"CSS file not found at {css_path}")
            govuk_css = ""  # Fallback to no CSS
        except Exception as e:
            print(f"Error loading CSS: {e}")
            govuk_css = ""
        
        # Try to use Jinja2 template, fall back to inline template if not found
        try:
            return render_template('gds_display.html',
                                title=display_config.get('title', 'Application Complete'),
                                sections_html=sections_html,
                                workflow_data_html=workflow_data_html,
                                completion_message=display_config.get('completion_message', 'Your application has been submitted.'),
                                service_name=self.service_name,
                                govuk_css=govuk_css)
        except Exception as e:
            print(f"Template error: {e}, falling back to inline template")
            print(f"CSS length: {len(govuk_css)} characters")
            # Fallback to inline template
            return render_template_string(template,
                                        title=display_config.get('title', 'Application Complete'),
                                        sections_html=Markup(''.join(sections_html)),
                                        workflow_data_html=Markup(workflow_data_html),
                                        completion_message=display_config.get('completion_message', 'Your application has been submitted.'),
                                        service_name=self.service_name,
                                        govuk_css=Markup(govuk_css))
    
    def render_gds_section(self, section: Dict[str, Any]) -> str:
        """Render a display section using GDS components."""
        section_title = section.get('title', 'Section')
        section_items = section.get('items', [])
        
        items_html = []
        for item in section_items:
            if isinstance(item, dict):
                label = item.get('label', 'Item')
                value = item.get('value', '')
                items_html.append(f'''
                <div class="govuk-summary-list__row">
                    <dt class="govuk-summary-list__key">{label}</dt>
                    <dd class="govuk-summary-list__value">{value}</dd>
                </div>
                ''')
            else:
                items_html.append(f'<p class="govuk-body">{item}</p>')
        
        if items_html and all('<div' in item for item in items_html):
            # Summary list format for key-value pairs
            return f'''
            <h2 class="govuk-heading-l">{section_title}</h2>
            <dl class="govuk-summary-list">
                {''.join(items_html)}
            </dl>
            '''
        elif items_html:
            # Regular paragraphs for text content
            return f'''
            <h2 class="govuk-heading-l">{section_title}</h2>
            {''.join(items_html)}
            '''
        else:
            return f'''
            <h2 class="govuk-heading-l">{section_title}</h2>
            <p class="govuk-body">No information to display.</p>
            '''
    
    def render_workflow_data(self, workflow_data=None) -> str:
        """Render workflow data using GDS summary list component."""
        # Use the workflow_data parameter passed from parent class
        if workflow_data is None:
            return '<p class="govuk-body">No workflow data available.</p>'
        
        workflow_params = dict(workflow_data)
        workflow_params.pop('workflow_token', None)  # Remove token from display
        
        if not workflow_params:
            return '<p class="govuk-body">No application details to display.</p>'
        
        # Render as GDS summary list
        data_html = []
        for key, value in workflow_params.items():
            # Handle different value types properly
            if isinstance(value, list):
                if len(value) == 1:
                    value = value[0]  # Flatten single-item lists
                else:
                    value = ', '.join(str(v) for v in value)  # Join multiple values
            
            # Convert to string and skip empty values
            value = str(value).strip()
            if not value:
                continue
                
            display_key = key.replace('_', ' ').title()
            
            # Special formatting for sensitive data
            if 'password' in key.lower() or 'secret' in key.lower():
                value = '••••••••'
            elif 'account' in key.lower() and 'number' in key.lower():
                # Mask account numbers
                value = '****' + str(value)[-4:] if len(str(value)) > 4 else value
            elif len(str(value)) > 100:
                # Truncate very long values
                value = str(value)[:100] + '...'
            
            data_html.append(f'''
            <div class="govuk-summary-list__row">
                <dt class="govuk-summary-list__key">{display_key}</dt>
                <dd class="govuk-summary-list__value">{value}</dd>
            </div>
            ''')
        
        if not data_html:
            return '<p class="govuk-body">No application details to display.</p>'
        
        return f'''
        <h2 class="govuk-heading-l">Your Application Details</h2>
        <dl class="govuk-summary-list">
            {''.join(data_html)}
        </dl>
        '''