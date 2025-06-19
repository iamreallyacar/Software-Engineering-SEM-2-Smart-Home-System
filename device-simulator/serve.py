"""
Simple HTTP server to serve the device simulator.
This solves CORS issues when accessing the Django API from the HTML file.
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

# Get the directory where this script is located
DEVICE_SIMULATOR_DIR = Path(__file__).parent

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler with CORS headers"""
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()
    
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.end_headers()

def start_server(port=8080):
    """Start the HTTP server"""
    os.chdir(DEVICE_SIMULATOR_DIR)
    
    with socketserver.TCPServer(("", port), CORSHTTPRequestHandler) as httpd:
        print(f"🚀 Device Simulator Server starting on port {port}")
        print(f"📱 Access the simulator at: http://localhost:{port}")
        print(f"📁 Serving files from: {DEVICE_SIMULATOR_DIR}")
        print(f"🔗 Make sure Django backend is running on: http://127.0.0.1:8000")
        print("\n💡 To stop the server, press Ctrl+C")
        
        # Try to open browser automatically
        try:
            webbrowser.open(f'http://localhost:{port}')
            print("🌐 Browser opened automatically")
        except:
            print("🌐 Please manually open http://localhost:{port} in your browser")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")

if __name__ == "__main__":
    start_server()
