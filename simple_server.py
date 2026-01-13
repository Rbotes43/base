#!/usr/bin/env python3
"""
Simple HTTP server for ASA Compliance Checker
Uses Python's built-in http.server module (no Flask needed)
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
from asa_compliance import ASAComplianceChecker
import os


class ComplianceHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Serve the HTML page"""
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('templates/index.html', 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404)

    def do_POST(self):
        """Handle compliance check requests"""
        if self.path == '/api/check-text':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            content = data.get('content', '')

            if not content:
                self.send_error(400, 'No content provided')
                return

            # Run compliance check
            checker = ASAComplianceChecker()
            results = checker.check_content(content)

            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(results).encode('utf-8'))
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        """Custom log format"""
        print(f"[{self.log_date_time_string()}] {format % args}")


def run_server(port=8000):
    """Start the HTTP server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, ComplianceHandler)

    print("=" * 70)
    print("🇬🇧  ASA COMPLIANCE TOOL - Simple HTTP Server")
    print("=" * 70)
    print(f"\n✅ Server running at: http://localhost:{port}")
    print(f"✅ Or try: http://127.0.0.1:{port}")
    print("\n📝 Open your browser and go to the URL above")
    print("\n⚠️  Note: Visual upload not supported in this simple version")
    print("   Use the full Flask app for image analysis features")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 70 + "\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
        httpd.shutdown()


if __name__ == '__main__':
    # Check if templates directory exists
    if not os.path.exists('templates/index.html'):
        print("❌ Error: templates/index.html not found!")
        print("Make sure you're running this from the base directory.")
        exit(1)

    run_server(8000)
