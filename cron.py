import sys
import os

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import NewsBot

def handler(request):
    """
    Vercel serverless function handler
    This gets called automatically by Vercel cron jobs
    """
    try:
        bot = NewsBot()
        bot.run()
        bot.cleanup_old_data(days=7)
        
        return {
            'statusCode': 200,
            'body': 'News bot executed successfully'
        }
    except Exception as e:
        print(f"Error in handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }
