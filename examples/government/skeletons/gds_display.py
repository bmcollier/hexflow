"""GDS Display application skeleton following UK Government Design System guidelines."""

import sys
import os
from flask import request, render_template_string
from typing import Dict, List, Any, Optional

# Add the parent directory to the path so we can import hexflow
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from hexflow.skeletons.display.app import DisplayApp


class GDSDisplayApp(DisplayApp):
    """Government Digital Service display application following GDS Design System."""
    
    def __init__(self, name: str = "gds-display-app", host: str = 'localhost', port: int = 8000):
        super().__init__(name=name, host=host, port=port)
        
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
        
        # GDS-compliant template
        template = '''
        <!DOCTYPE html>
        <html lang="en" class="govuk-template">
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
                /* Additional custom styles for display pages */
                .govuk-grid-column-two-thirds {
                    width: 100%;
                }
                
                @media (min-width: 40.0625em) {
                    .govuk-grid-column-two-thirds {
                        width: 66.6666%;
                        float: left;
                    }
                }
                
                .govuk-grid-row {
                    margin-right: -15px;
                    margin-left: -15px;
                }
                
                .govuk-grid-row:after {
                    content: "";
                    display: block;
                    clear: both;
                }
                
                [class*="govuk-grid-column"] {
                    box-sizing: border-box;
                    width: 100%;
                    padding: 0 15px;
                }
                
                /* Ensure summary lists display correctly */
                .govuk-summary-list {
                    font-family: "GDS Transport", arial, sans-serif;
                    -webkit-font-smoothing: antialiased;
                    -moz-osx-font-smoothing: grayscale;
                    font-weight: 400;
                    font-size: 16px;
                    line-height: 1.25;
                    color: #0b0c0c;
                    margin-top: 0;
                    margin-bottom: 20px;
                    border-collapse: collapse;
                    width: 100%;
                }
                
                .govuk-summary-list__row {
                    border-bottom: 1px solid #b1b4b6;
                }
                
                .govuk-summary-list__key {
                    font-weight: 700;
                    margin-top: 0;
                    margin-bottom: 5px;
                    padding: 10px 20px 10px 0;
                    border-bottom: 1px solid #b1b4b6;
                    width: 30%;
                    vertical-align: top;
                }
                
                .govuk-summary-list__value {
                    margin-top: 0;
                    margin-bottom: 5px;
                    padding: 10px 0;
                    border-bottom: 1px solid #b1b4b6;
                    word-wrap: break-word;
                    overflow-wrap: break-word;
                }
            </style>
        </head>
        <body class="govuk-template__body">
            <header class="govuk-header" role="banner" data-module="govuk-header">
                <div class="govuk-header__container govuk-width-container">
                    <div class="govuk-header__content">
                        <a href="#" class="govuk-header__link govuk-header__logotype">
                            <svg xmlns="http://www.w3.org/2000/svg" focusable="false" role="img" viewBox="0 0 324 60" height="30" width="162" fill="currentcolor" class="govuk-header__logotype" aria-label="GOV.UK">
                                <title>GOV.UK</title>
                                <g>
                                    <circle cx="20" cy="17.6" r="3.7"></circle>
                                    <circle cx="10.2" cy="23.5" r="3.7"></circle>
                                    <circle cx="3.7" cy="33.2" r="3.7"></circle>
                                    <circle cx="31.7" cy="30.6" r="3.7"></circle>
                                    <circle cx="43.3" cy="17.6" r="3.7"></circle>
                                    <circle cx="53.2" cy="23.5" r="3.7"></circle>
                                    <circle cx="59.7" cy="33.2" r="3.7"></circle>
                                    <circle cx="31.7" cy="30.6" r="3.7"></circle>
                                    <path d="M33.1,9.8c.2-.1.3-.3.5-.5l4.6,2.4v-6.8l-4.6,1.5c-.1-.2-.3-.3-.5-.5l1.9-5.9h-6.7l1.9,5.9c-.2.1-.3.3-.5.5l-4.6-1.5v6.8l4.6-2.4c.1.2.3.3.5.5l-2.6,8c-.9,2.8,1.2,5.7,4.1,5.7h0c3,0,5.1-2.9,4.1-5.7l-2.6-8ZM37,37.9s-3.4,3.8-4.1,6.1c2.2,0,4.2-.5,6.4-2.8l-.7,8.5c-2-2.8-4.4-4.1-5.7-3.8.1,3.1.5,6.7,5.8,7.2,3.7.3,6.7-1.5,7-3.8.4-2.6-2-4.3-3.7-1.6-1.4-4.5,2.4-6.1,4.9-3.2-1.9-4.5-1.8-7.7,2.4-10.9,3,4,2.6,7.3-1.2,11.1,2.4-1.3,6.2,0,4,4.6-1.2-2.8-3.7-2.2-4.2.2-.3,1.7.7,3.7,3,4.2,1.9.3,4.7-.9,7-5.9-1.3,0-2.4.7-3.9,1.7l2.4-8c.6,2.3,1.4,3.7,2.2,4.5.6-1.6.5-2.8,0-5.3l5,1.8c-2.6,3.6-5.2,8.7-7.3,17.5-7.4-1.1-15.7-1.7-24.5-1.7h0c-8.8,0-17.1.6-24.5,1.7-2.1-8.9-4.7-13.9-7.3-17.5l5-1.8c-.5,2.5-.6,3.7,0,5.3.8-.8,1.6-2.3,2.2-4.5l2.4,8c-1.5-1-2.6-1.7-3.9-1.7,2.3,5,5.2,6.2,7,5.9,2.3-.4,3.3-2.4,3-4.2-.5-2.4-3-3.1-4.2-.2-2.2-4.6,1.6-6,4-4.6-3.7-3.7-4.2-7.1-1.2-11.1,4.2,3.2,4.3,6.4,2.4,10.9,2.5-2.8,6.3-1.3,4.9,3.2-1.8-2.7-4.1-1-3.7,1.6.3,2.3,3.3,4.1,7,3.8,5.4-.5,5.7-4.2,5.8-7.2-1.3-.2-3.7,1-5.7,3.8l-.7-8.5c2.2,2.3,4.2,2.7,6.4,2.8-.7-2.3-4.1-6.1-4.1-6.1h10.6,0Z"></path>
                                </g>
                                <circle class="govuk-logo-dot" cx="226" cy="36" r="7.3"></circle>
                                <path d="M93.94 41.25c.4 1.81 1.2 3.21 2.21 4.62 1 1.4 2.21 2.41 3.61 3.21s3.21 1.2 5.22 1.2 3.61-.4 4.82-1c1.4-.6 2.41-1.4 3.21-2.41.8-1 1.4-2.01 1.61-3.01s.4-2.01.4-3.01v.14h-10.86v-7.02h20.07v24.08h-8.03v-5.56c-.6.8-1.38 1.61-2.19 2.41-.8.8-1.81 1.2-2.81 1.81-1 .4-2.21.8-3.41 1.2s-2.41.4-3.81.4a18.56 18.56 0 0 1-14.65-6.63c-1.6-2.01-3.01-4.41-3.81-7.02s-1.4-5.62-1.4-8.83.4-6.02 1.4-8.83a20.45 20.45 0 0 1 19.46-13.65c3.21 0 4.01.2 5.82.8 1.81.4 3.61 1.2 5.02 2.01 1.61.8 2.81 2.01 4.01 3.21s2.21 2.61 2.81 4.21l-7.63 4.41c-.4-1-1-1.81-1.61-2.61-.6-.8-1.4-1.4-2.21-2.01-.8-.6-1.81-1-2.81-1.4-1-.4-2.21-.4-3.61-.4-2.01 0-3.81.4-5.22 1.2-1.4.8-2.61 1.81-3.61 3.21s-1.61 2.81-2.21 4.62c-.4 1.81-.6 3.71-.6 5.42s.8 5.22.8 5.22Zm57.8-27.9c3.21 0 6.22.6 8.63 1.81 2.41 1.2 4.82 2.81 6.62 4.82S170.2 24.39 171 27s1.4 5.62 1.4 8.83-.4 6.02-1.4 8.83-2.41 5.02-4.01 7.02-4.01 3.61-6.62 4.82-5.42 1.81-8.63 1.81-6.22-.6-8.63-1.81-4.82-2.81-6.42-4.82-3.21-4.41-4.01-7.02-1.4-5.62-1.4-8.83.4-6.02 1.4-8.83 2.41-5.02 4.01-7.02 4.01-3.61 6.42-4.82 5.42-1.81 8.63-1.81Zm0 36.73c1.81 0 3.61-.4 5.02-1s2.61-1.81 3.61-3.01 1.81-2.81 2.21-4.41c.4-1.81.8-3.61.8-5.62 0-2.21-.2-4.21-.8-6.02s-1.2-3.21-2.21-4.62c-1-1.2-2.21-2.21-3.61-3.01s-3.21-1-5.02-1-3.61.4-5.02 1c-1.4.8-2.61 1.81-3.61 3.01s-1.81 2.81-2.21 4.62c-.4 1.81-.8 3.61-.8 5.62 0 2.41.2 4.21.8 6.02.4 1.81 1.2 3.21 2.21 4.41s2.21 2.21 3.61 3.01c1.4.8 3.21 1 5.02 1Zm36.32 7.96-12.24-44.15h9.83l8.43 32.77h.4l8.23-32.77h9.83L200.3 58.04h-12.24Zm74.14-7.96c2.18 0 3.51-.6 3.51-.6 1.2-.6 2.01-1 2.81-1.81s1.4-1.81 1.81-2.81a13 13 0 0 0 .8-4.01V13.9h8.63v28.15c0 2.41-.4 4.62-1.4 6.62-.8 2.01-2.21 3.61-3.61 5.02s-3.41 2.41-5.62 3.21-4.62 1.2-7.02 1.2-5.02-.4-7.02-1.2c-2.21-.8-4.01-1.81-5.62-3.21s-2.81-3.01-3.61-5.02-1.4-4.21-1.4-6.62V13.9h8.63v26.95c0 1.61.2 3.01.8 4.01.4 1.2 1.2 2.21 2.01 2.81.8.8 1.81 1.4 2.81 1.81 0 0 1.34.6 3.51.6Zm34.22-36.18v18.92l15.65-18.92h10.82l-15.03 17.32 16.03 26.83h-10.21l-11.44-20.21-5.62 6.22v13.99h-8.83V13.9"></path>
                            </svg>
                        </a>
                        <span class="govuk-header__product-name">Modular Builder Service</span>
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
        </body>
        </html>
        '''
        
        # Load clean, consistent GOV.UK CSS
        css_path = os.path.join(os.path.dirname(__file__), 'assets', 'govuk-clean.css')
        with open(css_path, 'r', encoding='utf-8') as f:
            govuk_css = f.read()
        
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