from hexflow.skeletons.casa.app import CasaApp
import os

class PaymentApp(CasaApp):
    """Dummy payment processing for fishing license application."""
    
    def __init__(self, name="payment", host='localhost', port=8003):
        super().__init__(name=name, host=host, port=port)
        
        # Set up custom template folder 
        custom_template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        if os.path.exists(custom_template_dir):
            self.app.template_folder = custom_template_dir
    
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
    
    def render_form(self, errors=None):
        """Override to use custom template with special checkbox handling."""
        from flask import render_template, request
        
        form_config = self.form_config
        errors = errors or {}
        
        # Build form fields HTML with custom styling
        fields_html = []
        for field in form_config.get('fields', []):
            if field['type'] == 'checkbox':
                field_html = self.render_payment_checkbox(field, errors.get(field['name'], ''))
            else:
                field_html = self.render_field(field, errors.get(field['name'], ''))
            fields_html.append(field_html)
        
        workflow_token = request.form.get('workflow_token', '') or request.args.get('workflow_token', '')
        
        # Try to use custom template first
        try:
            return render_template('payment_form.html',
                                title=form_config.get('title', 'Payment'),
                                fields_html=fields_html,
                                submit_text=form_config.get('submit_text', 'Process Payment'),
                                app_name=self.name,
                                workflow_token=workflow_token)
        except Exception:
            # Fall back to parent class behavior
            return super().render_form(errors)
    
    def render_payment_checkbox(self, field, error=''):
        """Render checkbox with payment-specific styling."""
        field_name = field['name']
        field_label = field.get('label', field_name.replace('_', ' ').title())
        field_value = field.get('value', 'yes')
        help_text = field.get('help_text', '')
        is_required = field.get('required', False)
        
        from flask import request
        is_checked = request.form.get(field_name, '') == field_value or request.args.get(field_name, '') == field_value
        
        error_html = f'<div class="error">{error}</div>' if error else ''
        help_html = f'<div class="help-text">{help_text}</div>' if help_text else ''
        required_class = 'required' if is_required else ''
        
        return f'''
        <div class="form-group">
            {error_html}
            <div class="checkbox-group {required_class}">
                <input type="checkbox" name="{field_name}" id="{field_name}" value="{field_value}" {'checked' if is_checked else ''} {'required' if is_required else ''}>
                <label for="{field_name}">{field_label}</label>
            </div>
            {help_html}
        </div>
        '''

if __name__ == "__main__":
    app = PaymentApp(name="payment", port=8003)
    app.run()