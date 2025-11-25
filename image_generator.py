from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap
from datetime import datetime
import os
from config import IMAGE_SETTINGS, DESIGN_COLORS, FONT_SIZES, OUTPUT_DIR

class ImageGenerator:
    def __init__(self):
        # Create output directory if it doesn't exist
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # Try to load fonts, fall back to default if not available
        try:
            self.headline_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", FONT_SIZES['headline'])
            self.subtext_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONT_SIZES['subtext'])
            self.source_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONT_SIZES['source'])
        except:
            # Fallback to default PIL font
            self.headline_font = ImageFont.load_default()
            self.subtext_font = ImageFont.load_default()
            self.source_font = ImageFont.load_default()
    
    def generate_post_image(self, processed_story, platform='instagram', news_image_path=None):
        """
        Generate a bold, modern image for social media
        news_image_path: Optional path to news article image to use as background
        Returns the file path of the generated image
        """
        # Get dimensions for platform
        settings = IMAGE_SETTINGS[platform]
        width, height = settings['width'], settings['height']
        
        # Create base image with gradient background or news image
        if news_image_path and os.path.exists(news_image_path):
            img = self._create_image_with_photo_background(news_image_path, width, height)
        else:
            img = self._create_gradient_background(width, height)
        
        draw = ImageDraw.Draw(img)
        
        # Add geometric shapes for modern look
        self._add_geometric_shapes(draw, width, height)
        
        # Add headline
        headline = self._truncate_text(processed_story['highlight'], 60)
        self._add_headline(draw, headline, width, height)
        
        # Add category tag
        self._add_category_tag(draw, processed_story['category'], width, height)
        
        # Add source attribution
        sources_text = ", ".join(processed_story['sources'][:2])
        self._add_source(draw, sources_text, width, height)
        
        # Add timestamp
        timestamp = datetime.now().strftime("%B %d, %Y")
        self._add_timestamp(draw, timestamp, width, height)
        
        # Add accent elements
        self._add_accent_elements(draw, width, height)
        
        # Save image
        filename = f"{OUTPUT_DIR}/post_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{platform}.png"
        img.save(filename, quality=95)
        
        print(f"✓ Generated image: {filename}")
        return filename
    
    def _create_gradient_background(self, width, height):
        """Create a gradient background"""
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        # Create vertical gradient
        start_color = DESIGN_COLORS['background_gradient'][0]
        end_color = DESIGN_COLORS['background_gradient'][1]
        
        for y in range(height):
            # Interpolate between start and end colors
            ratio = y / height
            r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
            
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        return img
    
    def _create_image_with_photo_background(self, photo_path, width, height):
        """Create background using news article photo with overlay"""
        try:
            # Load and resize the news image
            news_img = Image.open(photo_path)
            
            # Resize to cover the canvas
            img_ratio = news_img.width / news_img.height
            canvas_ratio = width / height
            
            if img_ratio > canvas_ratio:
                # Image is wider, fit to height
                new_height = height
                new_width = int(height * img_ratio)
            else:
                # Image is taller, fit to width
                new_width = width
                new_height = int(width / img_ratio)
            
            news_img = news_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Center crop
            left = (new_width - width) // 2
            top = (new_height - height) // 2
            news_img = news_img.crop((left, top, left + width, top + height))
            
            # Apply dark overlay for text readability
            overlay = Image.new('RGBA', (width, height), (0, 0, 0, 180))
            news_img = news_img.convert('RGBA')
            news_img = Image.alpha_composite(news_img, overlay)
            
            return news_img.convert('RGB')
            
        except Exception as e:
            print(f"Error using photo background: {str(e)}")
            # Fallback to gradient
            return self._create_gradient_background(width, height)
    
    def _add_geometric_shapes(self, draw, width, height):
        """Add bold geometric shapes for modern design"""
        # Large circle accent
        circle_radius = int(width * 0.3)
        draw.ellipse(
            [width - circle_radius - 50, -circle_radius//2, 
             width - 50, circle_radius//2],
            fill=self._hex_to_rgb(DESIGN_COLORS['primary']) + (40,)  # Semi-transparent
        )
        
        # Bottom left triangle accent
        triangle_points = [
            (0, height),
            (width * 0.2, height),
            (0, height - width * 0.2)
        ]
        draw.polygon(triangle_points, fill=self._hex_to_rgb(DESIGN_COLORS['secondary']) + (40,))
    
    def _add_headline(self, draw, text, width, height):
        """Add main headline text"""
        # Wrap text to fit width
        max_width = int(width * 0.85)
        wrapped_lines = self._wrap_text(text, self.headline_font, max_width, draw)
        
        # Calculate starting position (centered vertically)
        y_position = height // 3
        
        for line in wrapped_lines:
            # Get text bounding box for centering
            bbox = draw.textbbox((0, 0), line, font=self.headline_font)
            text_width = bbox[2] - bbox[0]
            
            x = (width - text_width) // 2
            
            # Add text shadow for better readability
            shadow_offset = 4
            draw.text((x + shadow_offset, y_position + shadow_offset), line, 
                     fill=(0, 0, 0, 128), font=self.headline_font)
            
            # Main text
            draw.text((x, y_position), line, 
                     fill=self._hex_to_rgb(DESIGN_COLORS['text']), 
                     font=self.headline_font)
            
            y_position += bbox[3] - bbox[1] + 15
    
    def _add_category_tag(self, draw, category, width, height):
        """Add a category tag/badge"""
        # Create rounded rectangle for category
        tag_text = category.upper()
        tag_padding = 20
        
        bbox = draw.textbbox((0, 0), tag_text, font=self.source_font)
        tag_width = bbox[2] - bbox[0] + tag_padding * 2
        tag_height = bbox[3] - bbox[1] + tag_padding
        
        x = 40
        y = 40
        
        # Draw rounded rectangle background
        draw.rounded_rectangle(
            [x, y, x + tag_width, y + tag_height],
            radius=10,
            fill=self._hex_to_rgb(DESIGN_COLORS['accent'])
        )
        
        # Draw text
        draw.text(
            (x + tag_padding, y + tag_padding//2),
            tag_text,
            fill=self._hex_to_rgb(DESIGN_COLORS['dark']),
            font=self.source_font
        )
    
    def _add_source(self, draw, text, width, height):
        """Add source attribution at bottom"""
        source_text = f"📰 {text}"
        bbox = draw.textbbox((0, 0), source_text, font=self.source_font)
        
        x = 40
        y = height - 100
        
        draw.text((x, y), source_text, 
                 fill=self._hex_to_rgb(DESIGN_COLORS['text']) + (200,),
                 font=self.source_font)
    
    def _add_timestamp(self, draw, text, width, height):
        """Add timestamp at bottom"""
        time_text = f"🕐 {text}"
        bbox = draw.textbbox((0, 0), time_text, font=self.source_font)
        
        x = 40
        y = height - 60
        
        draw.text((x, y), time_text, 
                 fill=self._hex_to_rgb(DESIGN_COLORS['text']) + (200,),
                 font=self.source_font)
    
    def _add_accent_elements(self, draw, width, height):
        """Add small accent lines/elements"""
        # Top accent line
        line_width = width * 0.15
        draw.rectangle(
            [40, 110, 40 + line_width, 115],
            fill=self._hex_to_rgb(DESIGN_COLORS['secondary'])
        )
    
    def _wrap_text(self, text, font, max_width, draw):
        """Wrap text to fit within max_width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            
            if bbox[2] - bbox[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def _truncate_text(self, text, max_length):
        """Truncate text to max length"""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
    
    def _hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Test function
if __name__ == "__main__":
    generator = ImageGenerator()
    
    # Test data
    test_story = {
        'highlight': 'Bangladesh Cricket Team Makes Historic Victory Against India',
        'category': 'sports',
        'sources': ['daily_star', 'bdnews24']
    }
    
    # Generate for both platforms
    instagram_img = generator.generate_post_image(test_story, 'instagram')
    facebook_img = generator.generate_post_image(test_story, 'facebook')
    
    print(f"✓ Test images generated!")
    print(f"  Instagram: {instagram_img}")
    print(f"  Facebook: {facebook_img}")
