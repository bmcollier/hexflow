#!/usr/bin/env python3
"""IT Setup and Equipment - Employee Onboarding Step 3"""

import sys
import os
from flask import request

# Add the parent directory to the path so we can import modularbuilder
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from modularbuilder.skeletons.casa.app import CasaApp


class ITSetupApp(CasaApp):
    """IT setup and equipment requests for new employees."""
    
    def __init__(self, name="it-setup", host='localhost', port=8003):
        super().__init__(name=name, host=host, port=port)
    
    def setup_form(self):
        """Define IT setup form fields."""
        return {
            'title': 'Employee Onboarding - IT Setup',
            'fields': [
                {
                    'name': 'laptop_type',
                    'label': 'Laptop Preference',
                    'type': 'select',
                    'required': True,
                    'options': [
                        {'value': 'macbook_air_m2', 'text': 'MacBook Air M2 13"'},
                        {'value': 'macbook_pro_14', 'text': 'MacBook Pro 14" M3'},
                        {'value': 'macbook_pro_16', 'text': 'MacBook Pro 16" M3'},
                        {'value': 'thinkpad_x1', 'text': 'Lenovo ThinkPad X1 Carbon'},
                        {'value': 'dell_xps_13', 'text': 'Dell XPS 13'},
                        {'value': 'surface_laptop', 'text': 'Microsoft Surface Laptop'}
                    ]
                },
                {
                    'name': 'monitor_setup',
                    'label': 'Monitor Setup',
                    'type': 'select',
                    'required': True,
                    'options': [
                        {'value': 'single_24', 'text': 'Single 24" Monitor'},
                        {'value': 'dual_24', 'text': 'Dual 24" Monitors'},
                        {'value': 'single_27', 'text': 'Single 27" Monitor'},
                        {'value': 'dual_27', 'text': 'Dual 27" Monitors'},
                        {'value': 'ultrawide', 'text': '34" Ultrawide Monitor'},
                        {'value': 'none', 'text': 'No External Monitor (Laptop Only)'}
                    ]
                },
                {
                    'name': 'mobile_phone',
                    'label': 'Company Mobile Phone',
                    'type': 'select',
                    'required': True,
                    'options': [
                        {'value': 'iphone_15', 'text': 'iPhone 15'},
                        {'value': 'iphone_15_pro', 'text': 'iPhone 15 Pro'},
                        {'value': 'samsung_s24', 'text': 'Samsung Galaxy S24'},
                        {'value': 'pixel_8', 'text': 'Google Pixel 8'},
                        {'value': 'none', 'text': 'No Company Phone Required'}
                    ]
                },
                {
                    'name': 'software_access',
                    'label': 'Software Access Required',
                    'type': 'textarea',
                    'required': True,
                    'placeholder': 'List software, tools, and services you need access to (e.g., Jira, Figma, Salesforce, AWS, GitHub)',
                    'rows': 4
                },
                {
                    'name': 'development_tools',
                    'label': 'Development Tools (if applicable)',
                    'type': 'select',
                    'required': False,
                    'options': [
                        {'value': '', 'text': 'Not applicable / Not a developer'},
                        {'value': 'basic', 'text': 'Basic (Git, IDE, Browser)'},
                        {'value': 'frontend', 'text': 'Frontend (Node.js, npm, React tools)'},
                        {'value': 'backend', 'text': 'Backend (Docker, Databases, API tools)'},
                        {'value': 'fullstack', 'text': 'Full-stack (All development tools)'},
                        {'value': 'devops', 'text': 'DevOps (CI/CD, Infrastructure tools)'},
                        {'value': 'data', 'text': 'Data Science (Python, Jupyter, ML tools)'}
                    ]
                },
                {
                    'name': 'vpn_access',
                    'label': 'VPN Access Required',
                    'type': 'select',
                    'required': True,
                    'options': [
                        {'value': 'standard', 'text': 'Standard VPN Access'},
                        {'value': 'privileged', 'text': 'Privileged VPN Access'},
                        {'value': 'none', 'text': 'No VPN Access Required'}
                    ]
                },
                {
                    'name': 'cloud_accounts',
                    'label': 'Cloud Service Accounts',
                    'type': 'textarea',
                    'required': False,
                    'placeholder': 'List cloud services you need access to (AWS, Azure, GCP, etc.) and required permission levels',
                    'rows': 3
                },
                {
                    'name': 'special_requirements',
                    'label': 'Special IT Requirements',
                    'type': 'textarea',
                    'required': False,
                    'placeholder': 'Any additional IT setup needs or accessibility requirements',
                    'rows': 3
                }
            ],
            'validation': {
                'software_access': {
                    'min_length': 10,
                    'message': 'Please provide details about the software access you need'
                }
            },
            'submit_text': 'Continue to HR Documentation'
        }
    
    def render_form(self, errors=None):
        """Render the form with personalization."""
        # Get employee details from previous steps
        employee_name = request.args.get('full_name', 'New Employee')
        department = request.args.get('department', '').replace('_', ' ').title()
        
        # Update the form title with personalization
        form_config = self.form_config.copy()
        form_config['title'] = f'Employee Onboarding - IT Setup for {employee_name}'
        if department:
            form_config['title'] += f' ({department})'
        
        # Temporarily replace the form config for rendering
        original_config = self.form_config
        self.form_config = form_config
        
        # Call the parent render method
        result = super().render_form(errors)
        
        # Restore original config
        self.form_config = original_config
        
        return result


if __name__ == "__main__":
    app = ITSetupApp()
    app.run(debug=True)