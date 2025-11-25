from http.server import BaseHTTPRequestHandler
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import NewsBot

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            bot = NewsBot()
            bot.run()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"statusCode": 200, "body": "News bot executed successfully"}')
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_msg = f'{{"statusCode": 500, "body": "Error: {str(e)}"}}'
            self.wfile.write(error_msg.encode())
