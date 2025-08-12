#!/usr/bin/env python3
"""Job Details Collection - Employee Onboarding Step 2"""

import sys
import os
from flask import request

# Add the parent directory to the path so we can import modularbuilder
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from modularbuilder.skeletons.casa.app import CasaApp


class JobDetailsApp(CasaApp):
    """Job details collection form for new employees."""
    
    def __init__(self, name="job-details", host='localhost', port=8002):
        super().__init__(name=name, host=host, port=port)
    
    def setup_form(self):
        """Define job details form fields."""
        return {
            'title': 'Employee Onboarding - Job Details',
            'fields': [
                {
                    'name': 'department',
                    'label': 'Department',
                    'type': 'select',
                    'required': True,
                    'options': [
                        {'value': 'engineering', 'text': 'Engineering'},
                        {'value': 'product', 'text': 'Product Management'},
                        {'value': 'design', 'text': 'Design & UX'},
                        {'value': 'marketing', 'text': 'Marketing'},
                        {'value': 'sales', 'text': 'Sales'},
                        {'value': 'customer_success', 'text': 'Customer Success'},
                        {'value': 'finance', 'text': 'Finance'},
                        {'value': 'hr', 'text': 'Human Resources'},
                        {'value': 'operations', 'text': 'Operations'},
                        {'value': 'legal', 'text': 'Legal'}
                    ]
                },
                {
                    'name': 'job_title',
                    'label': 'Job Title',
                    'type': 'text',
                    'required': True,
                    'placeholder': 'e.g. Senior Software Engineer, Product Manager'
                },
                {
                    'name': 'employment_type',
                    'label': 'Employment Type',
                    'type': 'select',
                    'required': True,
                    'options': [
                        {'value': 'full_time', 'text': 'Full-time'},
                        {'value': 'part_time', 'text': 'Part-time'},
                        {'value': 'contract', 'text': 'Contract'},
                        {'value': 'intern', 'text': 'Internship'}
                    ]
                },
                {
                    'name': 'start_date',
                    'label': 'Start Date',
                    'type': 'date',
                    'required': True
                },
                {
                    'name': 'manager_name',
                    'label': 'Direct Manager',
                    'type': 'text',
                    'required': True,
                    'placeholder': 'Full name of your direct manager'
                },
                {
                    'name': 'office_location',
                    'label': 'Primary Office Location',
                    'type': 'select',
                    'required': True,
                    'options': [
                        {'value': 'london', 'text': 'London, UK'},
                        {'value': 'edinburgh', 'text': 'Edinburgh, UK'},
                        {'value': 'manchester', 'text': 'Manchester, UK'},
                        {'value': 'remote_uk', 'text': 'Remote (UK)'},
                        {'value': 'hybrid', 'text': 'Hybrid (Office + Remote)'}
                    ]
                },
                {
                    'name': 'salary_band',
                    'label': 'Salary Band',
                    'type': 'select',
                    'required': True,
                    'options': [
                        {'value': 'band_1', 'text': 'Band 1 (Junior)'},
                        {'value': 'band_2', 'text': 'Band 2 (Mid-level)'},
                        {'value': 'band_3', 'text': 'Band 3 (Senior)'},
                        {'value': 'band_4', 'text': 'Band 4 (Lead)'},
                        {'value': 'band_5', 'text': 'Band 5 (Principal/Director)'}
                    ]
                },
                {
                    'name': 'security_clearance',
                    'label': 'Security Clearance Required',
                    'type': 'select',
                    'required': True,
                    'options': [
                        {'value': 'none', 'text': 'None Required'},
                        {'value': 'basic', 'text': 'Basic DBS Check'},
                        {'value': 'enhanced', 'text': 'Enhanced DBS Check'},
                        {'value': 'security_cleared', 'text': 'Security Clearance (SC)'},
                        {'value': 'developed_vetting', 'text': 'Developed Vetting (DV)'}
                    ]
                }
            ],
            'validation': {
                'job_title': {
                    'min_length': 2,
                    'message': 'Please enter a valid job title'
                },
                'manager_name': {
                    'min_length': 2,
                    'message': 'Please enter your manager\'s full name'
                }
            },
            'submit_text': 'Continue to IT Setup'
        }
    
    def render_form(self, errors=None):
        """Render the form with personalization."""
        # Get employee name from previous step for personalization
        employee_name = request.args.get('full_name', 'New Employee')
        
        # Update the form title with personalization
        form_config = self.form_config.copy()
        form_config['title'] = f'Employee Onboarding - Job Details for {employee_name}'
        
        # Temporarily replace the form config for rendering
        original_config = self.form_config
        self.form_config = form_config
        
        # Call the parent render method
        result = super().render_form(errors)
        
        # Restore original config
        self.form_config = original_config
        
        return result


if __name__ == "__main__":
    app = JobDetailsApp()
    app.run(debug=True)