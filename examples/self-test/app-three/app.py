"""Simple test application 3 - subclasses http-base with Complete button."""

import sys
import os

# Add the modularbuilder package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from modularbuilder.skeletons.http_base.app import HTTPBaseApp


class AppThree(HTTPBaseApp):
    """Test application 3 - final app with Complete button."""
    
    def setup_routes(self):
        """Setup routes with Complete button functionality."""
        @self.app.route('/')
        def index():
            return '''
            <h1>App Three</h1>
            <p>Modular-Builder: Running</p>
            <p>This is the final application in the workflow.</p>
            <form action="http://localhost:8000/next" method="get">
                <input type="hidden" name="from" value="app-three">
                <button type="submit" style="padding: 10px 20px; font-size: 16px;">Complete ✓</button>
            </form>
            ''', 200


if __name__ == "__main__":
    app = AppThree(name="app-three", port=8003)
    app.run()