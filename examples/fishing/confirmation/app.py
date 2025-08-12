from hexflow.skeletons.http_base.app import HTTPBaseApp
from flask import request
import random

class ConfirmationApp(HTTPBaseApp):
    """Display confirmation page with all collected details from the fishing license workflow."""
    
    def setup_routes(self):
        """Setup routes for the confirmation page."""
        @self.app.route('/', methods=['GET', 'POST'])
        def index():
            # Get all workflow data passed from router (prioritize POST)
            workflow_data = dict(request.form) if request.method == 'POST' else dict(request.args)
            workflow_token = workflow_data.pop('workflow_token', '')
            
            # Extract data with defaults
            full_name = workflow_data.get('full_name', 'Not provided')
            address_line1 = workflow_data.get('address_line1', '')
            address_line2 = workflow_data.get('address_line2', '')
            city = workflow_data.get('city', '')
            postcode = workflow_data.get('postcode', '')
            license_type = workflow_data.get('license_type', 'Not selected')
            start_date = workflow_data.get('start_date', 'Not specified')
            disability_concession = 'Yes' if workflow_data.get('disability_concession') else 'No'
            senior_concession = 'Yes' if workflow_data.get('senior_concession') else 'No'
            payment_method = workflow_data.get('payment_method', 'Not specified')
            
            # Build full address
            address_parts = [address_line1]
            if address_line2:
                address_parts.append(address_line2)
            address_parts.extend([city, postcode])
            full_address = ', '.join(filter(None, address_parts))
            
            # Format concessions
            concessions = []
            if disability_concession == 'Yes':
                concessions.append('Disability Concession')
            if senior_concession == 'Yes':
                concessions.append('Senior Concession (65+)')
            concessions_text = ', '.join(concessions) if concessions else 'None'
            
            # Generate reference and transaction IDs
            reference_number = f"{random.randint(100000, 999999)}"
            transaction_id = f"{random.randint(10000000, 99999999)}"
            
            # Map license types to prices (simplified)
            license_prices = {
                'coarse': '£30.00',
                'trout': '£37.00', 
                'salmon': '£82.00',
                'short-term-coarse': '£6.00',
                'short-term-trout': '£12.00',
                'short-term-salmon': '£27.00'
            }
            license_price = license_prices.get(license_type, '£0.00')
            
            return f'''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Fishing License Application - Confirmation</title>
                <style>
                    body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #2563eb; color: white; padding: 20px; text-align: center; margin-bottom: 30px; }}
                    .section {{ background-color: #f8fafc; padding: 20px; margin-bottom: 20px; border-left: 4px solid #2563eb; }}
                    .section h3 {{ margin-top: 0; color: #1e40af; }}
                    .detail {{ margin-bottom: 10px; }}
                    .label {{ font-weight: bold; display: inline-block; min-width: 150px; }}
                    .success {{ background-color: #10b981; color: white; padding: 15px; text-align: center; font-size: 18px; margin-bottom: 20px; }}
                    .reference {{ background-color: #fbbf24; padding: 15px; text-align: center; font-size: 16px; font-weight: bold; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Fishing License Application Complete</h1>
                    <p>Your application has been successfully submitted</p>
                </div>
                
                <div class="success">
                    ✅ Application Successfully Processed
                </div>
                
                <div class="reference">
                    Reference Number: FL-2024-{reference_number}
                </div>
                
                <div class="section">
                    <h3>Personal Details</h3>
                    <div class="detail">
                        <span class="label">Full Name:</span>
                        <span id="full_name">{full_name}</span>
                    </div>
                    <div class="detail">
                        <span class="label">Address:</span>
                        <span id="address">{full_address}</span>
                    </div>
                </div>
                
                <div class="section">
                    <h3>License Details</h3>
                    <div class="detail">
                        <span class="label">License Type:</span>
                        <span id="license_type">{license_type}</span>
                    </div>
                    <div class="detail">
                        <span class="label">Start Date:</span>
                        <span id="start_date">{start_date}</span>
                    </div>
                    <div class="detail">
                        <span class="label">Concessions:</span>
                        <span id="concessions">{concessions_text}</span>
                    </div>
                </div>
                
                <div class="section">
                    <h3>Payment Information</h3>
                    <div class="detail">
                        <span class="label">Payment Method:</span>
                        <span id="payment_method">{payment_method}</span>
                    </div>
                    <div class="detail">
                        <span class="label">Amount Paid:</span>
                        <span id="amount">{license_price}</span>
                    </div>
                    <div class="detail">
                        <span class="label">Transaction ID:</span>
                        <span id="transaction_id">TXN-{transaction_id}</span>
                    </div>
                </div>
                
                <div class="section">
                    <h3>Next Steps</h3>
                    <p>Your fishing license will be sent to you within 5-10 business days at the address provided above.</p>
                    <p>You can also download a temporary license certificate valid for 72 hours while you wait for your physical license to arrive.</p>
                    <p><strong>Important:</strong> Please save this confirmation page for your records. You may need the reference number if you need to contact us about your application.</p>
                </div>
                
                <div style="text-align: center; margin-top: 40px; padding: 20px; border-top: 2px solid #e5e7eb;">
                    <p>Thank you for your fishing license application!</p>
                    <p style="font-size: 14px; color: #6b7280;">
                        For questions about your application, please contact us at: <br>
                        Phone: 0300 123 1234 | Email: fishing.licenses@environment-agency.gov.uk
                    </p>
                </div>
            </body>
            </html>
            ''', 200

if __name__ == "__main__":
    app = ConfirmationApp(name="confirmation", port=8004)
    app.run()