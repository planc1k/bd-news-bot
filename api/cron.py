from http.server import BaseHTTPRequestHandler
import sys
import os
cat > api/cron.py << 'EOF'
from http.server import BaseHTTPRequestHandler
import sys
import os

# Add parent directory to path to import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import NewsBot

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Run the news bot
            bot = NewsBot()
            bot.run()
            
            # Return success response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"statusCode": 200, "body": "News bot executed successfully"}')
            
        except Exception as e:
            # Return error response
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_msg = f'{{"statusCode": 500, "body": "Error: {str(e)}"}}'
            self.wfile.write(error_msg.encode())
