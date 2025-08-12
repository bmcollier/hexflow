"""Simple test application 2 - subclasses http-base with Next button."""

import sys
import os

# Add the modularbuilder package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from modularbuilder.skeletons.http_base.app import HTTPBaseApp


class AppTwo(HTTPBaseApp):
    """Test application 2 - with Next button to proceed in workflow."""
    
    def setup_routes(self):
        """Setup routes with Next button functionality."""
        @self.app.route('/')
        def index():
            return '''
            <h1>App Two</h1>
            <p>Modular-Builder: Running</p>
            <p>This is the second application in the workflow.</p>
            <form action="http://localhost:8000/next" method="get">
                <input type="hidden" name="from" value="app-two">
                <button type="submit" style="padding: 10px 20px; font-size: 16px;">Next →</button>
            </form>
            ''', 200


if __name__ == "__main__":
    app = AppTwo(name="app-two", port=8002)
    app.run()