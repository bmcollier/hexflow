from hexflow.skeletons.casa.app import CasaApp

class NameAndAddressApp(CasaApp):
    """Collect name and address information for British fishing license applicants."""
    
    def setup_form(self):
        """Define form fields for name and address collection."""
        return {
            'title': 'Fishing License Application - Personal Details',
            'description': 'Please provide your full name and address.',
            'fields': [
                {
                    'name': 'full_name',
                    'label': 'Full Name',
                    'type': 'text',
                    'required': True,
                    'placeholder': 'Enter your full legal name'
                },
                {
                    'name': 'address_line1',
                    'label': 'Address Line 1',
                    'type': 'text',
                    'required': True,
                    'placeholder': 'House number and street name'
                },
                {
                    'name': 'address_line2',
                    'label': 'Address Line 2',
                    'type': 'text',
                    'required': False,
                    'placeholder': 'Optional - apartment, suite, etc.'
                },
                {
                    'name': 'city',
                    'label': 'City/Town',
                    'type': 'text',
                    'required': True,
                    'placeholder': 'Enter your city or town'
                },
                {
                    'name': 'postcode',
                    'label': 'Postcode',
                    'type': 'text',
                    'required': True,
                    'placeholder': 'e.g. SW1A 1AA'
                }
            ],
            'validation': {
                'full_name': {
                    'min_length': 2,
                    'message': 'Full name must be at least 2 characters'
                },
                'postcode': {
                    'pattern': r'^[A-Z]{1,2}[0-9][A-Z0-9]?\s?[0-9][A-Z]{2}$',
                    'message': 'Please enter a valid UK postcode'
                }
            }
        }

if __name__ == "__main__":
    app = NameAndAddressApp(name="name-and-address", port=8001)
    app.run()