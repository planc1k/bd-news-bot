from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap
from datetime import datetime
import os
from config import IMAGE_SETTINGS, DESIGN_COLORS, FONT_SIZES, OUTPUT_DIR, BRAND_NAME, LOGO_PATH, LOGO_WIDTH, LOGO_POSITION, SHOW_BRAND_TEXT

class ScrollUpImageGenerator:
    """
    Image generator matching Scroll Up Today brand style:
    - Red highlight boxes on key phrases
    - White or black backgrounds
    - Bold, clean typography
    - Real news photos
    - ScrollUp Today branding
    """
    
    def __init__(self):
        # Create output directory if it doesn't exist
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # Load fonts
        try:
            self.headline_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
            self.subtext_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
            self.source_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
            self.brand_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
        except:
            self.headline_font = ImageFont.load_default()
            self.subtext_font = ImageFont.load_default()
            self.source_font = ImageFont.load_default()
            self.brand_font = ImageFont.load_default()
    
    def generate_post_image(self, processed_story, platform='instagram', news_image_path=None):
        """
        Generate image matching Scroll Up Today style
        """
        settings = IMAGE_SETTINGS[platform]
        width, height = settings['width'], settings['height']
        
        # Choose style based on whether we have a news image
        if news_image_path and os.path.exists(news_image_path):
            # Style 1: News photo with text overlay (like your curfew/railway posts)
            img = self._create_photo_style(processed_story, width, height, news_image_path)
        else:
            # Style 2: White/black background with bold text (like your text posts)
            img = self._create_text_style(processed_story, width, height)
        
        # Save image
        filename = f"{OUTPUT_DIR}/post_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{platform}.png"
        img.save(filename, quality=95)
        
        print(f"✓ Generated Scroll Up Today style image: {filename}")
        return filename
    
    def _create_text_style(self, story, width, height):
        """
        Create text-focused design with white/black background
        Matches your posts like the railway announcement
        """
        # Choose background (alternate between white and black)
        use_white_bg = hash(story['highlight']) % 2 == 0
        
        if use_white_bg:
            img = Image.new('RGB', (width, height), DESIGN_COLORS['background_white'])
            text_color = (0, 0, 0)
            highlight_color = self._hex_to_rgb(DESIGN_COLORS['highlight_bg'])
        else:
            img = Image.new('RGB', (width, height), DESIGN_COLORS['background_black'])
            text_color = (255, 255, 255)
            highlight_color = self._hex_to_rgb(DESIGN_COLORS['secondary'])
        
        draw = ImageDraw.Draw(img)
        
        # Add headline with red highlight effect
        headline = story['highlight']
        self._add_highlighted_headline(draw, headline, width, height, text_color, highlight_color)
        
        # Add source and date at bottom
        self._add_source_date(draw, story['sources'], width, height, text_color)
        
        # Add ScrollUp Today branding
        self._add_branding(draw, width, height, text_color)
        
        return img
    
    def _create_photo_style(self, story, width, height, photo_path):
        """
        Create design with news photo
        Matches your curfew post style
        """
        try:
            # Load news photo
            news_img = Image.open(photo_path)
            
            # Determine layout: photo on bottom, text on top (like your curfew post)
            # Create white background for top half
            img = Image.new('RGB', (width, height), (255, 255, 255))
            
            # Resize and place photo in bottom half
            photo_height = int(height * 0.55)  # 55% for photo
            photo_width = width
            
            # Resize photo to fit
            news_img = self._resize_and_crop(news_img, photo_width, photo_height)
            
            # Paste photo on bottom
            img.paste(news_img, (0, height - photo_height))
            
            draw = ImageDraw.Draw(img)
            
            # Add headline on white background (top half)
            self._add_headline_on_white(draw, story['highlight'], width, int(height * 0.45))
            
            # Add source and date on white background
            y_position = int(height * 0.38)
            self._add_source_date_compact(draw, story['sources'], width, y_position, (100, 100, 100))
            
            # Add branding on photo (bottom right)
            self._add_branding_on_photo(draw, width, height)
            
            return img
            
        except Exception as e:
            print(f"Error creating photo style: {e}")
            return self._create_text_style(story, width, height)
    
    def _add_highlighted_headline(self, draw, text, width, height, text_color, highlight_color):
        """
        Add headline with red highlight boxes around key phrases
        Matches your style of highlighting important words
        """
        # Split into words
        words = text.split()
        
        # Find key words to highlight (words longer than 5 chars or all caps)
        words_to_highlight = set()
        for i, word in enumerate(words):
            if len(word) > 6 or (word.isupper() and len(word) > 3):
                words_to_highlight.add(word)
        
        # If no key words found, highlight every 3rd-4th word
        if not words_to_highlight and len(words) >= 3:
            words_to_highlight = set([words[1], words[min(3, len(words)-1)]])
        
        # Calculate starting position
        y_start = height // 3
        x_margin = 60
        line_spacing = 80
        max_line_width = width - (x_margin * 2)
        
        # Build lines
        lines = []
        current_line = []
        current_width = 0
        
        for word in words:
            word_bbox = draw.textbbox((0, 0), word + " ", font=self.headline_font)
            word_width = word_bbox[2] - word_bbox[0]
            
            if current_width + word_width > max_line_width and current_line:
                lines.append(current_line)
                current_line = [word]
                current_width = word_width
            else:
                current_line.append(word)
                current_width += word_width
        
        if current_line:
            lines.append(current_line)
        
        # Draw lines
        y_position = y_start
        
        for line_words in lines:
            x = x_margin
            
            for word in line_words:
                word_bbox = draw.textbbox((x, y_position), word, font=self.headline_font)
                
                # Check if word should be highlighted
                if word in words_to_highlight:
                    padding = 10
                    draw.rectangle(
                        [word_bbox[0] - padding, word_bbox[1] - 5,
                         word_bbox[2] + padding, word_bbox[3] + 5],
                        fill=highlight_color
                    )
                
                # Draw word
                draw.text((x, y_position), word, fill=text_color, font=self.headline_font)
                x = word_bbox[2] + 20
            
            y_position += line_spacing
    
    def _add_headline_on_white(self, draw, text, width, available_height):
        """
        Add headline on white background (for photo posts)
        """
        words = text.split()
        
        # Find important phrase to highlight (first 3-5 words)
        if len(words) > 5:
            highlight_phrase = ' '.join(words[1:4])  # Middle words
            remaining = words[0] + ' ' + ' '.join(words[4:])
        else:
            highlight_phrase = ' '.join(words[:2])
            remaining = ' '.join(words[2:])
        
        y_position = 50
        x_margin = 50
        
        # Draw first part
        if words[0]:
            draw.text((x_margin, y_position), words[0], fill=(0, 0, 0), font=self.subtext_font)
            y_position += 60
        
        # Draw highlighted phrase with red background
        bbox = draw.textbbox((x_margin, y_position), highlight_phrase, font=self.subtext_font)
        padding = 15
        draw.rectangle(
            [bbox[0] - padding, bbox[1] - 10, bbox[2] + padding, bbox[3] + 10],
            fill=self._hex_to_rgb(DESIGN_COLORS['highlight_bg'])
        )
        draw.text((x_margin, y_position), highlight_phrase, fill=(255, 255, 255), font=self.subtext_font)
        
        y_position += 65
        
        # Draw remaining text
        if remaining:
            draw.text((x_margin, y_position), remaining, fill=(0, 0, 0), font=self.subtext_font)
    
    def _add_source_date(self, draw, sources, width, height, text_color):
        """
        Add source and date at bottom (your standard format)
        """
        source_text = f"Source: {', '.join(sources[:2])}"
        date_text = f"Date: {datetime.now().strftime('%dth %b %y')}"
        
        y_position = height - 120
        x_margin = 60
        
        # Draw source on left
        draw.text((x_margin, y_position), source_text, fill=text_color, font=self.source_font)
        
        # Draw date on right
        date_bbox = draw.textbbox((0, 0), date_text, font=self.source_font)
        date_width = date_bbox[2] - date_bbox[0]
        draw.text((width - date_width - x_margin, y_position), date_text, fill=text_color, font=self.source_font)
    
    def _add_source_date_compact(self, draw, sources, width, y_position, color):
        """
        Compact source and date (for photo posts)
        """
        source_text = f"Source: {', '.join(sources[:1])}"
        date_text = f"Date: {datetime.now().strftime('%dth %b %y')}"
        
        x_margin = 50
        
        draw.text((x_margin, y_position), source_text, fill=color, font=self.source_font)
        
        date_bbox = draw.textbbox((0, 0), date_text, font=self.source_font)
        date_width = date_bbox[2] - date_bbox[0]
        draw.text((width - date_width - x_margin, y_position), date_text, fill=color, font=self.source_font)
    
    def _add_branding(self, draw, width, height, text_color):
        """
        Add ScrollUp Today branding (bottom right)
        Uses actual logo if available, otherwise text + orange dot
        """
        # Try to load and use actual logo
        if os.path.exists(LOGO_PATH):
            self._add_logo_image(draw, width, height, text_color, on_photo=False)
        else:
            # Fallback to text-based branding
            self._add_text_branding(draw, width, height, text_color)
    
    def _add_logo_image(self, draw, width, height, text_color, on_photo=False):
        """
        Add actual logo image to the post
        on_photo: True if placing on photo background (adds shadow)
        """
        try:
            # Load logo
            logo = Image.open(LOGO_PATH)
            
            # Resize logo maintaining aspect ratio
            aspect_ratio = logo.height / logo.width
            logo_width = LOGO_WIDTH
            logo_height = int(logo_width * aspect_ratio)
            logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
            
            # Calculate position based on config
            margin = 40 if on_photo else 50
            if LOGO_POSITION == 'bottom-right':
                x = width - logo_width - margin
                y = height - logo_height - margin
            elif LOGO_POSITION == 'bottom-left':
                x = margin
                y = height - logo_height - margin
            elif LOGO_POSITION == 'top-right':
                x = width - logo_width - margin
                y = margin
            else:  # top-left
                x = margin
                y = margin
            
            # Add shadow if on photo for better visibility
            if on_photo and logo.mode == 'RGBA':
                # Create shadow
                shadow = Image.new('RGBA', logo.size, (0, 0, 0, 0))
                shadow_draw = ImageDraw.Draw(shadow)
                shadow_draw.rectangle([5, 5, logo.width, logo.height], fill=(0, 0, 0, 100))
                shadow = shadow.filter(ImageFilter.GaussianBlur(radius=3))
                
                # Paste shadow first
                img = draw._image
                img.paste(shadow, (x, y), shadow)
            
            # Paste logo
            if logo.mode == 'RGBA':
                img = draw._image
                img.paste(logo, (x, y), logo)
            else:
                img = draw._image
                img.paste(logo, (x, y))
            
            # Add text alongside logo if configured
            if SHOW_BRAND_TEXT:
                text_x = x - 200  # Position text to the left of logo
                text_y = y + (logo_height // 2) - 15
                
                if on_photo:
                    # Add shadow for text on photo
                    shadow_offset = 2
                    draw.text((text_x + shadow_offset, text_y + shadow_offset), 
                             BRAND_NAME, fill=(0, 0, 0, 150), font=self.brand_font)
                
                draw.text((text_x, text_y), BRAND_NAME, fill=text_color, font=self.brand_font)
                
        except Exception as e:
            print(f"⚠️  Error loading logo from {LOGO_PATH}: {e}")
            print(f"   Using text-based branding instead")
            # Fallback to text branding
            if on_photo:
                self._add_text_branding_on_photo(draw, width, height)
            else:
                self._add_text_branding(draw, width, height, text_color)
    
    def _add_text_branding(self, draw, width, height, text_color):
        """Fallback text-based branding with orange dot"""
        brand_text = BRAND_NAME
        
        # Position in bottom right corner
        bbox = draw.textbbox((0, 0), brand_text, font=self.brand_font)
        text_width = bbox[2] - bbox[0]
        
        x = width - text_width - 60
        y = height - 70
        
        # Draw brand name
        draw.text((x, y), brand_text, fill=text_color, font=self.brand_font)
        
        # Add orange accent dot/circle (like your sunrise logo)
        circle_radius = 8
        circle_x = x - 25
        circle_y = y + 15
        draw.ellipse(
            [circle_x - circle_radius, circle_y - circle_radius,
             circle_x + circle_radius, circle_y + circle_radius],
            fill=self._hex_to_rgb(DESIGN_COLORS['accent'])
        )
    
    def _add_branding_on_photo(self, draw, width, height):
        """
        Add branding on photo background (white text with shadow)
        Uses actual logo if available
        """
        # Try to load and use actual logo
        if os.path.exists(LOGO_PATH):
            self._add_logo_image(draw, width, height, (255, 255, 255), on_photo=True)
        else:
            # Fallback to text-based branding
            self._add_text_branding_on_photo(draw, width, height)
    
    def _add_text_branding_on_photo(self, draw, width, height):
        """Fallback text branding for photo backgrounds"""
        brand_text = BRAND_NAME
        
        bbox = draw.textbbox((0, 0), brand_text, font=self.brand_font)
        text_width = bbox[2] - bbox[0]
        
        x = width - text_width - 50
        y = height - 60
        
        # Text shadow for visibility
        shadow_offset = 2
        draw.text((x + shadow_offset, y + shadow_offset), brand_text, 
                 fill=(0, 0, 0, 150), font=self.brand_font)
        
        # White text
        draw.text((x, y), brand_text, fill=(255, 255, 255), font=self.brand_font)
        
        # Orange accent
        circle_radius = 8
        circle_x = x - 25
        circle_y = y + 15
        draw.ellipse(
            [circle_x - circle_radius, circle_y - circle_radius,
             circle_x + circle_radius, circle_y + circle_radius],
            fill=self._hex_to_rgb(DESIGN_COLORS['accent'])
        )
    
    def _resize_and_crop(self, img, target_width, target_height):
        """Resize and crop image to fit dimensions"""
        img_ratio = img.width / img.height
        target_ratio = target_width / target_height
        
        if img_ratio > target_ratio:
            new_height = target_height
            new_width = int(target_height * img_ratio)
        else:
            new_width = target_width
            new_height = int(target_width / img_ratio)
        
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Center crop
        left = (new_width - target_width) // 2
        top = (new_height - target_height) // 2
        img = img.crop((left, top, left + target_width, top + target_height))
        
        return img
    
    def _hex_to_rgb(self, hex_color):
        """Convert hex to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# For backward compatibility, alias the new class
ImageGenerator = ScrollUpImageGenerator
