"""GDS Display application skeleton following UK Government Design System guidelines."""

import sys
import os
from flask import request, render_template_string, render_template
from typing import Dict, List, Any, Optional

# Add the parent directory to the path so we can import hexflow
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from hexflow.skeletons.display.app import DisplayApp


class GDSDisplayApp(DisplayApp):
    """Government Digital Service display application following GDS Design System."""
    
    def __init__(self, name: str = "gds-display-app", host: str = 'localhost', port: int = 8000):
        super().__init__(name=name, host=host, port=port)
        
        # Set up template folder for Jinja2
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        if os.path.exists(template_dir):
            self.app.template_folder = template_dir
        
    def render_display(self) -> str:
        """Render the display HTML using GDS Design System styling."""
        display_config = self.display_config
        workflow_token = request.args.get('workflow_token', '')
        
        # Build sections HTML
        sections_html = []
        for section in display_config.get('sections', []):
            section_html = self.render_gds_section(section)
            sections_html.append(section_html)
        
        # Get workflow data if requested
        workflow_data_html = ''
        if display_config.get('show_workflow_data', False) and workflow_token:
            workflow_data_html = self.render_workflow_data()
        
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
                        <span class="govuk-header__product-name">Hexflow Service</span>
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
            
            <!-- GOV.UK Frontend JavaScript -->
            <script type="module">
                import { initAll } from '/assets/javascripts/govuk-frontend.min.js'
                initAll()
            </script>
        </body>
        </html>
        '''
        
        # Load GOV.UK Frontend CSS
        css_path = os.path.join(os.path.dirname(__file__), 'assets', 'govuk-frontend.min.css')
        with open(css_path, 'r', encoding='utf-8') as f:
            govuk_css = f.read()
        
        # Try to use Jinja2 template, fall back to inline template if not found
        try:
            return render_template('gds_display.html',
                                title=display_config.get('title', 'Application Complete'),
                                sections_html=sections_html,
                                workflow_data_html=workflow_data_html,
                                completion_message=display_config.get('completion_message', 'Your application has been submitted.'),
                                govuk_css=govuk_css)
        except Exception as e:
            print(f"Template error: {e}, falling back to inline template")
            # Fallback to inline template
            return render_template_string(template,
                                        title=display_config.get('title', 'Application Complete'),
                                        sections_html=''.join(sections_html),
                                        workflow_data_html=workflow_data_html,
                                        completion_message=display_config.get('completion_message', 'Your application has been submitted.'),
                                        govuk_css=govuk_css)
    
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
                <tr class="govuk-summary-list__row">
                    <dt class="govuk-summary-list__key">{label}</dt>
                    <dd class="govuk-summary-list__value">{value}</dd>
                </tr>
                ''')
            else:
                items_html.append(f'<p class="govuk-body">{item}</p>')
        
        if items_html and all('<tr' in item for item in items_html):
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
    
    def render_workflow_data(self) -> str:
        """Render workflow data using GDS summary list component."""
        workflow_token = request.args.get('workflow_token', '')
        if not workflow_token:
            return '<p class="govuk-body">No workflow data available.</p>'
        
        # Get all workflow parameters passed to this app
        workflow_params = dict(request.args)
        workflow_params.pop('workflow_token', None)  # Remove token from display
        
        if not workflow_params:
            return '<p class="govuk-body">No application details to display.</p>'
        
        # Render as GDS summary list
        data_html = []
        for key, value in workflow_params.items():
            if isinstance(value, list) and len(value) == 1:
                value = value[0]  # Flatten single-item lists from URL params
            
            # Skip empty values
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
            <tr class="govuk-summary-list__row">
                <dt class="govuk-summary-list__key">{display_key}</dt>
                <dd class="govuk-summary-list__value">{value}</dd>
            </tr>
            ''')
        
        if not data_html:
            return '<p class="govuk-body">No application details to display.</p>'
        
        return f'''
        <h2 class="govuk-heading-l">Your Application Details</h2>
        <dl class="govuk-summary-list">
            {''.join(data_html)}
        </dl>
        '''