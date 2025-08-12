"""Simple confirmation display app demonstrating workflow data access."""

import sys
import os

# Add the hexflow package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from hexflow.skeletons.display.app import DisplayApp


class ConfirmationApp(DisplayApp):
    """Display confirmation page with workflow data."""
    
    def setup_display(self, workflow_data=None):
        """Setup display using workflow data."""
        workflow_data = workflow_data or {}
        
        # Create dynamic content based on workflow data
        sections = []
        
        if workflow_data:
            sections.append({
                'title': 'Your Information',
                'items': [
                    {'label': key.replace('_', ' ').title(), 'value': value} 
                    for key, value in workflow_data.items()
                ]
            })
        
        return {
            'title': 'Workflow Complete',
            'sections': sections,
            'show_workflow_data': True,
            'completion_message': 'Thank you! Your workflow has been completed successfully.'
        }


if __name__ == "__main__":
    app = ConfirmationApp(name="confirmation", port=8004)
    app.run()