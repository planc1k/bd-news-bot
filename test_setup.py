#!/usr/bin/env python3
"""
Quick test script to verify the news bot setup
This tests core functionality without requiring API keys
"""

import os
import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    try:
        import feedparser
        import requests
        from bs4 import BeautifulSoup
        from PIL import Image, ImageDraw, ImageFont
        import json
        print("✓ All required packages installed")
        return True
    except ImportError as e:
        print(f"✗ Missing package: {str(e)}")
        print("  Run: pip install -r requirements.txt")
        return False

def test_config():
    """Test if configuration file is valid"""
    print("\n🧪 Testing configuration...")
    try:
        import config
        print(f"✓ Config loaded")
        print(f"  - News sources: {len(config.NEWS_SOURCES)}")
        print(f"  - Focus topics: {len(config.FOCUS_TOPICS)}")
        print(f"  - Max posts/day: {config.MAX_POSTS_PER_DAY}")
        return True
    except Exception as e:
        print(f"✗ Config error: {str(e)}")
        return False

def test_news_collector():
    """Test news collection (without actually scraping)"""
    print("\n🧪 Testing news collector...")
    try:
        from news_collector import NewsCollector
        collector = NewsCollector()
        print("✓ News collector initialized")
        print(f"  - Configured sources: {len(collector.headers)}")
        return True
    except Exception as e:
        print(f"✗ News collector error: {str(e)}")
        return False

def test_image_generator():
    """Test image generator by creating a sample image"""
    print("\n🧪 Testing image generator...")
    try:
        from image_generator import ImageGenerator
        generator = ImageGenerator()
        
        # Create test image
        test_story = {
            'highlight': 'Test News: Bangladesh Tech Innovation',
            'category': 'technology',
            'sources': ['test_source']
        }
        
        image_path = generator.generate_post_image(test_story, 'instagram')
        
        if os.path.exists(image_path):
            print(f"✓ Image generated successfully")
            print(f"  - Path: {image_path}")
            
            # Check image properties
            from PIL import Image
            img = Image.open(image_path)
            print(f"  - Size: {img.size[0]}x{img.size[1]}")
            return True
        else:
            print("✗ Image not created")
            return False
            
    except Exception as e:
        print(f"✗ Image generator error: {str(e)}")
        return False

def test_env_file():
    """Check if .env file exists"""
    print("\n🧪 Checking environment setup...")
    if os.path.exists('.env'):
        print("✓ .env file found")
        
        # Check if it has content
        with open('.env', 'r') as f:
            content = f.read()
            if 'your_groq_api_key_here' in content:
                print("  ⚠️  .env file needs your actual API keys")
                print("  → Edit .env and add your Groq API key")
            else:
                print("  ✓ .env appears to be configured")
        return True
    else:
        print("⚠️  .env file not found")
        print("  → Copy .env.example to .env")
        print("  → Add your API keys")
        return False

def test_directory_structure():
    """Verify directory structure"""
    print("\n🧪 Checking directory structure...")
    
    required_files = [
        'main.py',
        'news_collector.py',
        'ai_processor.py',
        'image_generator.py',
        'social_poster.py',
        'config.py',
        'requirements.txt',
        'README.md'
    ]
    
    all_good = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} missing")
            all_good = False
    
    return all_good

def main():
    print("="*60)
    print("🤖 BANGLADESH NEWS BOT - Setup Test")
    print("="*60)
    
    results = []
    
    # Run all tests
    results.append(("Directory Structure", test_directory_structure()))
    results.append(("Python Imports", test_imports()))
    results.append(("Configuration", test_config()))
    results.append(("Environment File", test_env_file()))
    results.append(("News Collector", test_news_collector()))
    results.append(("Image Generator", test_image_generator()))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status} - {test_name}")
    
    print(f"\n  Score: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your bot is ready to run.")
        print("\n📝 Next steps:")
        print("  1. Add your Groq API key to .env file")
        print("  2. Run: python main.py")
        print("  3. Check generated_posts/ for images")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
    
    print("="*60)

if __name__ == "__main__":
    main()
