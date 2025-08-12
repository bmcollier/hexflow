from modularbuilder.skeletons.casa.app import CasaApp

class PaymentApp(CasaApp):
    """Dummy payment processing for fishing license application."""
    
    def setup_form(self):
        """Define form fields for payment processing (dummy implementation)."""
        return {
            'title': 'Fishing License Application - Payment',
            'description': 'Please review your order and confirm payment. This is a demonstration - no actual payment will be processed.',
            'fields': [
                {
                    'name': 'payment_method',
                    'label': 'Payment Method',
                    'type': 'select',
                    'required': True,
                    'options': [
                        {'value': 'card', 'text': 'Credit/Debit Card'},
                        {'value': 'paypal', 'text': 'PayPal'},
                        {'value': 'bank_transfer', 'text': 'Bank Transfer'}
                    ]
                },
                {
                    'name': 'cardholder_name',
                    'label': 'Cardholder Name',
                    'type': 'text',
                    'required': False,
                    'placeholder': 'Name as it appears on card (demo only)'
                },
                {
                    'name': 'card_number',
                    'label': 'Card Number',
                    'type': 'text',
                    'required': False,
                    'placeholder': '1234 5678 9012 3456 (demo only)'
                },
                {
                    'name': 'terms_accepted',
                    'label': 'I accept the terms and conditions',
                    'type': 'checkbox',
                    'required': True,
                    'value': 'accepted',
                    'help_text': 'You must accept the terms and conditions to proceed'
                },
                {
                    'name': 'confirm_payment',
                    'label': 'I confirm this payment is correct',
                    'type': 'checkbox',
                    'required': True,
                    'value': 'confirmed',
                    'help_text': 'Please confirm you wish to proceed with payment'
                }
            ],
            'validation': {
                'payment_method': {
                    'required': True,
                    'message': 'Please select a payment method'
                },
                'terms_accepted': {
                    'required': True,
                    'message': 'You must accept the terms and conditions'
                },
                'confirm_payment': {
                    'required': True,
                    'message': 'You must confirm your payment to proceed'
                }
            }
        }

if __name__ == "__main__":
    app = PaymentApp(name="payment", port=8003)
    app.run()