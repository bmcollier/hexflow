"""Base HTTP application skeleton using Flask."""

from flask import Flask


class HTTPBaseApp:
    """Base HTTP application that can be subclassed."""
    
    def __init__(self, name: str = "http-base", host: str = 'localhost', port: int = 8000):
        self.host = host
        self.port = port
        self.app = Flask(name)
        self.setup_routes()
    
    def setup_routes(self):
        """Setup default routes. Override in subclasses to add more routes."""
        @self.app.route('/', methods=['GET', 'POST'])
        def index():
            return 'Modular-Builder: Running', 200
    
    def run(self, debug: bool = False):
        """Start the Flask server."""
        self.app.run(host=self.host, port=self.port, debug=debug)
    
    def get_app(self):
        """Return the Flask app instance for WSGI deployment."""
        return self.app


if __name__ == "__main__":
    app = HTTPBaseApp()
    app.run()