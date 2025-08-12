#!/usr/bin/env python3
"""Welcome Confirmation - Employee Onboarding Final Step"""

import sys
import os
from flask import request

# Add the parent directory to the path so we can import modularbuilder
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from modularbuilder.skeletons.display import DisplayApp


class WelcomeConfirmationApp(DisplayApp):
    """Welcome confirmation page for completed employee onboarding."""
    
    def __init__(self, name="welcome-confirmation", host='localhost', port=8005):
        super().__init__(name=name, host=host, port=port)
    
    def setup_display(self):
        """Configure the welcome confirmation display."""
        return {
            'title': 'Welcome to the Team! 🎉',
            'sections': [
                {
                    'title': 'Onboarding Complete',
                    'items': [
                        'Congratulations! You have successfully completed the employee onboarding process.',
                        'All your information has been recorded and your accounts are being set up.',
                        'Please review all the details below to ensure everything is correct.'
                    ]
                }
            ],
            'show_workflow_data': True,
            'completion_message': 'Welcome to the company! Your IT equipment will be prepared and ready for your start date. You will receive a welcome email with additional information and next steps within 24 hours.'
        }
    
    def render_workflow_data(self) -> str:
        """Render all onboarding data from the four forms."""
        workflow_token = request.args.get('workflow_token', '')
        if not workflow_token:
            return '<div class="workflow-data"><div class="empty-data">No onboarding data available</div></div>'
        
        # Get all workflow parameters passed to this app
        workflow_params = dict(request.args)
        workflow_params.pop('workflow_token', None)  # Remove token from display
        
        if not workflow_params:
            return '<div class="workflow-data"><div class="empty-data">No onboarding details to display</div></div>'
        
        # Organize data into sections based on the four forms
        personal_data = {}
        job_data = {}
        it_data = {}
        hr_data = {}
        
        # Categorize the data based on field names
        for key, value in workflow_params.items():
            if isinstance(value, list) and len(value) == 1:
                value = value[0]  # Flatten single-item lists from URL params
            
            # Personal information (Form 1)
            if key in ['full_name', 'email', 'phone', 'date_of_birth', 'address_line_1', 
                      'address_line_2', 'city', 'postcode', 'emergency_contact_name', 
                      'emergency_contact_phone', 'emergency_contact_relationship']:
                personal_data[key] = value
                
            # Job details (Form 2)
            elif key in ['department', 'job_title', 'employment_type', 'start_date', 
                        'manager_name', 'office_location', 'salary_band', 'security_clearance']:
                job_data[key] = value
                
            # IT setup (Form 3)
            elif key in ['laptop_type', 'monitor_setup', 'mobile_phone', 'software_access', 
                        'development_tools', 'vpn_access', 'cloud_accounts', 'special_requirements']:
                it_data[key] = value
                
            # HR documentation (Form 4)
            elif key in ['national_insurance', 'bank_name', 'account_holder_name', 'sort_code', 
                        'account_number', 'tax_code', 'pension_scheme', 'health_insurance', 
                        'life_insurance', 'beneficiary_name', 'beneficiary_relationship', 
                        'holiday_entitlement', 'work_from_home', 'dietary_requirements']:
                hr_data[key] = value
            else:
                # Any other data goes in personal for now
                personal_data[key] = value
        
        sections_html = []
        
        # Section 1: Personal Information
        if personal_data:
            personal_html = self._render_data_section("👤 Personal Information", personal_data)
            sections_html.append(personal_html)
        
        # Section 2: Job Details
        if job_data:
            job_html = self._render_data_section("💼 Job Details", job_data)
            sections_html.append(job_html)
        
        # Section 3: IT Setup
        if it_data:
            it_html = self._render_data_section("💻 IT Setup & Equipment", it_data)
            sections_html.append(it_html)
        
        # Section 4: HR Documentation
        if hr_data:
            hr_html = self._render_data_section("📋 HR Documentation & Benefits", hr_data)
            sections_html.append(hr_html)
        
        if not sections_html:
            return '<div class="workflow-data"><div class="empty-data">No onboarding details to display</div></div>'
        
        return f'''
        <div class="workflow-data">
            {''.join(sections_html)}
        </div>
        '''
    
    def _render_data_section(self, title: str, data: dict) -> str:
        """Render a section of workflow data."""
        if not data:
            return ''
        
        data_html = []
        for key, value in data.items():
            # Skip empty values and documentation confirmations
            if not value or key == 'documentation_complete':
                continue
                
            display_key = key.replace('_', ' ').title()
            
            # Special formatting for specific fields
            if key == 'date_of_birth':
                display_key = 'Date of Birth'
            elif key == 'national_insurance':
                display_key = 'National Insurance Number'
            elif key == 'sort_code':
                display_key = 'Bank Sort Code'
            elif key == 'account_number':
                display_key = 'Bank Account Number'
                # Mask account number for security
                value = '****' + str(value)[-4:] if len(str(value)) > 4 else value
            elif 'software' in key or 'requirements' in key or 'dietary' in key:
                # For text areas, limit display length
                if len(str(value)) > 100:
                    value = str(value)[:100] + '...'
            
            data_html.append(f'''
            <div class="data-item">
                <span class="data-label">{display_key}:</span>
                <span class="data-value">{value}</span>
            </div>
            ''')
        
        return f'''
        <div class="section">
            <div class="step-title">{title}</div>
            {''.join(data_html) if data_html else '<div class="empty-data">No data in this section</div>'}
        </div>
        '''


if __name__ == "__main__":
    app = WelcomeConfirmationApp()
    app.run(debug=True)