"""GDS Casa application skeleton following UK Government Design System guidelines."""

import sys
import os
from flask import request, render_template_string, render_template
from typing import Dict, List, Any, Optional

# Add the parent directory to the path so we can import hexflow
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from hexflow.skeletons.casa.app import CasaApp


class GDSCasaApp(CasaApp):
    """Government Digital Service form-based application following GDS Design System."""
    
    def __init__(self, name: str = "gds-casa-app", host: str = 'localhost', port: int = 8000, service_name: str = None):
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
        def serve_casa_assets(filename):
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
        
        print(f"DEBUG: Serving asset {filename}")
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
            
            print(f"DEBUG: Content-Type set to: {response.headers.get('Content-Type')}")
            return response
        except Exception as e:
            print(f"ERROR serving {filename}: {e}")
            raise
        
    def render_form(self, errors: Dict[str, str] = None) -> str:
        """Render the form HTML using GDS Design System styling."""
        form_config = self.form_config
        errors = errors or {}
        
        # Log validation errors if any
        if errors:
            print(f"Form validation errors: {list(errors.keys())}")

                # Build form fields HTML
        fields_html = []
        for field in form_config.get('fields', []):
            field_html = self.render_gds_field(field, errors.get(field['name'], ''))
            fields_html.append(field_html)
        
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
            
            <!-- GOV.UK Frontend CSS -->
            <style>
                {{ govuk_css|safe }}
            </style>
            
            <style>
                /* Minor customizations for enhanced forms */
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
                            <h1 class="govuk-heading-xl">{{ title }}</h1>
                            
                            <form action="http://localhost:8000/next" method="post" novalidate>
                                <input type="hidden" name="from" value="{{ app_name }}">
                                <input type="hidden" name="workflow_token" value="{{ workflow_token }}">
                                
                                {{ fields_html|safe }}
                                
                                <div class="govuk-button-group">
                                    <button type="submit" name="action" value="submit" class="govuk-button" data-module="govuk-button">
                                        {{ submit_text }}
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </main>
            </div>
            
            <!-- GOV.UK Frontend JavaScript would go here if available -->
        </body>
        </html>
        '''
        
        workflow_token = request.form.get('workflow_token', '') or request.args.get('workflow_token', '')
        
        # Load GOV.UK Frontend CSS
        css_path = os.path.join(os.path.dirname(__file__), 'assets', 'govuk-frontend.min.css')
        with open(css_path, 'r', encoding='utf-8') as f:
            govuk_css = f.read()
        
        # Try to use Jinja2 template, fall back to inline template if not found
        try:
            print(f"DEBUG: Attempting to render gds_form.html with service_name: {self.service_name}")
            return render_template('gds_form.html',
                                title=form_config.get('title', 'Government Service'),
                                fields_html=fields_html,
                                submit_text=form_config.get('submit_text', 'Continue'),
                                app_name=self.name,
                                workflow_token=workflow_token,
                                service_name=self.service_name,
                                govuk_css=govuk_css)
        except Exception as e:
            print(f"Jinja2 template not found, using inline template fallback: {e}")
            # Fallback to inline template for backward compatibility
            return render_template_string(template, 
                                        title=form_config.get('title', 'Government Service'),
                                        fields_html=''.join(fields_html),
                                        submit_text=form_config.get('submit_text', 'Continue'),
                                        app_name=self.name,
                                        workflow_token=workflow_token,
                                        service_name=self.service_name,
                                        govuk_css=govuk_css)
    
    def render_gds_field(self, field: Dict[str, Any], error: str = '') -> str:
        """Render a single form field using GDS Design System components."""
        field_type = field.get('type', 'text')
        field_name = field['name']
        field_label = field.get('label', field_name.replace('_', ' ').title())
        field_required = field.get('required', False)
        field_options = field.get('options', [])
        field_value = request.form.get(field_name, '') or request.args.get(field_name, '')
        field_hint = field.get('help_text', '')
        field_placeholder = field.get('placeholder', '')
        
        # GDS error styling
        error_class = 'govuk-form-group--error' if error else ''
        input_error_class = 'govuk-input--error' if error else ''
        
        error_html = ''
        if error:
            error_html = f'''
            <span id="{field_name}-error" class="govuk-error-message">
                <span class="govuk-error-message__icon" aria-hidden="true">!</span>
                <span class="govuk-visually-hidden">Error:</span> {error}
            </span>
            '''
        
        hint_html = ''
        if field_hint:
            hint_html = f'<div id="{field_name}-hint" class="govuk-hint">{field_hint}</div>'
        
        if field_type == 'select':
            options_html = ['<option value="">Choose an option</option>']
            for option in field_options:
                if isinstance(option, dict):
                    value = option['value']
                    text = option['text']
                else:
                    value = text = option
                
                selected = 'selected' if field_value == value else ''
                options_html.append(f'<option value="{value}" {selected}>{text}</option>')
            
            field_html = f'''
            <div class="govuk-form-group {error_class}">
                <label class="govuk-label govuk-label--s" for="{field_name}">
                    {field_label}
                </label>
                {hint_html}
                {error_html}
                <select class="govuk-select" id="{field_name}" name="{field_name}" {"required" if field_required else ""}>
                    {''.join(options_html)}
                </select>
            </div>
            '''
        
        elif field_type == 'textarea':
            rows = field.get('rows', 5)
            field_html = f'''
            <div class="govuk-form-group {error_class}">
                <label class="govuk-label govuk-label--s" for="{field_name}">
                    {field_label}
                </label>
                {hint_html}
                {error_html}
                <textarea class="govuk-textarea {input_error_class}" id="{field_name}" name="{field_name}" 
                         rows="{rows}" {"required" if field_required else ""}>{field_value}</textarea>
            </div>
            '''
        
        elif field_type == 'checkbox':
            checkbox_value = field.get('value', 'yes')
            checked = 'checked' if field_value == checkbox_value else ''
            field_html = f'''
            <div class="govuk-form-group {error_class}">
                {error_html}
                <div class="govuk-checkboxes__item">
                    <input class="govuk-checkboxes__input" id="{field_name}" name="{field_name}" 
                           type="checkbox" value="{checkbox_value}" {checked} {"required" if field_required else ""}>
                    <label class="govuk-label govuk-checkboxes__label" for="{field_name}">
                        {field_label}
                    </label>
                    {hint_html}
                </div>
            </div>
            '''
        
        else:  # text, email, tel, date, etc.
            field_html = f'''
            <div class="govuk-form-group {error_class}">
                <label class="govuk-label govuk-label--s" for="{field_name}">
                    {field_label}
                </label>
                {hint_html}
                {error_html}
                <input class="govuk-input {input_error_class}" id="{field_name}" name="{field_name}" 
                       type="{field_type}" value="{field_value}" 
                       {"placeholder='" + field_placeholder + "'" if field_placeholder else ""}
                       {"required" if field_required else ""}>
            </div>
            '''
        
        return field_html