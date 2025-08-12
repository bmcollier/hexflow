from modularbuilder.skeletons.casa.app import CasaApp

class LicenseTypeApp(CasaApp):
    """Allow users to select their fishing license type and duration."""
    
    def setup_form(self):
        """Define form fields for license type selection."""
        return {
            'title': 'Fishing License Application - License Selection',
            'description': 'Please select the type of fishing license you would like to purchase.',
            'fields': [
                {
                    'name': 'license_type',
                    'label': 'License Type',
                    'type': 'select',
                    'required': True,
                    'options': [
                        {'value': 'coarse', 'text': 'Coarse Fishing License (£30/year)'},
                        {'value': 'trout', 'text': 'Trout and Coarse License (£37/year)'},
                        {'value': 'salmon', 'text': 'Salmon and Sea Trout License (£82/year)'},
                        {'value': 'short-term-coarse', 'text': 'Short Term Coarse (1 day - £6)'},
                        {'value': 'short-term-trout', 'text': 'Short Term Trout and Coarse (1 day - £12)'},
                        {'value': 'short-term-salmon', 'text': 'Short Term Salmon (1 day - £27)'}
                    ]
                },
                {
                    'name': 'start_date',
                    'label': 'License Start Date',
                    'type': 'date',
                    'required': True,
                    'help_text': 'When would you like your license to begin?'
                },
                {
                    'name': 'disability_concession',
                    'label': 'Disability Concession',
                    'type': 'checkbox',
                    'value': 'yes',
                    'help_text': 'Check if you qualify for a disability concession (50% discount)'
                },
                {
                    'name': 'senior_concession',
                    'label': 'Senior Concession (65+)',
                    'type': 'checkbox',
                    'value': 'yes',
                    'help_text': 'Check if you are 65 or older (applies to some license types)'
                }
            ],
            'validation': {
                'license_type': {
                    'required': True,
                    'message': 'Please select a license type'
                },
                'start_date': {
                    'required': True,
                    'message': 'Please select a start date for your license'
                }
            }
        }

if __name__ == "__main__":
    app = LicenseTypeApp(name="license-type", port=8002)
    app.run()