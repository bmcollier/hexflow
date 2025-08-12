"""Simple test application 1 - subclasses http-base with Next button."""

import sys
import os

# Add the hexflow package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from hexflow.skeletons.http_base.app import HTTPBaseApp


class AppOne(HTTPBaseApp):
    """Test application 1 - with Next button to proceed in workflow."""
    
    def setup_routes(self):
        """Setup routes with Next button functionality."""
        @self.app.route('/')
        def index():
            return '''
            <h1>App One</h1>
            <p>Modular-Builder: Running</p>
            <p>This is the first application in the workflow.</p>
            <form action="http://localhost:8000/next" method="get">
                <input type="hidden" name="from" value="app-one">
                <button type="submit" style="padding: 10px 20px; font-size: 16px;">Next →</button>
            </form>
            ''', 200


if __name__ == "__main__":
    app = AppOne(name="app-one", port=8001)
    app.run()