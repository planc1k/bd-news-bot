# 🎨 HOW TO ADD YOUR SCROLLUP TODAY LOGO

## 📍 Quick Answer

Put your logo file here:
```
bd-news-bot/
  └── assets/
       └── scrollup_logo.png  ← Your logo goes here!
```

That's it! The bot will automatically use it.

## 📋 Step-by-Step Instructions

### 1. **Prepare Your Logo**

**Best Format:**
- PNG with **transparent background** (recommended)
- Your orange sunrise burst logo
- Square or slightly horizontal aspect ratio
- High resolution (at least 300x300px)

**Alternative Formats:**
- PNG with white/black background (will work)
- JPG (but no transparency)

### 2. **Save Logo to Assets Folder**

```bash
# Navigate to your project
cd bd-news-bot

# Create assets folder if it doesn't exist
mkdir -p assets

# Copy your logo
# Option 1: Copy from desktop
cp ~/Desktop/scrollup_logo.png assets/

# Option 2: Download from your computer
# Just drag and drop your logo into the assets/ folder
```

**File Name:** Must be exactly `scrollup_logo.png`

### 3. **Test It**

```bash
python main.py
```

Check `generated_posts/` - your **actual logo** will be on every image!

## ⚙️ Configuration Options

### Change Logo Size

Edit `config.py`:
```python
LOGO_WIDTH = 150  # Change this number

# Examples:
LOGO_WIDTH = 100  # Smaller logo
LOGO_WIDTH = 200  # Bigger logo
```

### Change Logo Position

Edit `config.py`:
```python
LOGO_POSITION = 'bottom-right'  # Current

# Options:
LOGO_POSITION = 'bottom-right'  # ← Recommended (matches your posts)
LOGO_POSITION = 'bottom-left'
LOGO_POSITION = 'top-right'
LOGO_POSITION = 'top-left'
```

### Show/Hide Brand Text

Edit `config.py`:
```python
SHOW_BRAND_TEXT = True   # Shows "ScrollUp Today" + logo
SHOW_BRAND_TEXT = False  # Shows only logo
```

**Recommended:** `True` for better brand recognition

## 🎨 Logo Placement Examples

### Option 1: Logo + Text (Recommended)
```
┌─────────────────────────┐
│                         │
│   HEADLINE TEXT         │
│                         │
│                         │
│                         │
│                         │
│   ScrollUp Today [LOGO] │ ← Both text and logo
└─────────────────────────┘
```

### Option 2: Logo Only
```
┌─────────────────────────┐
│                         │
│   HEADLINE TEXT         │
│                         │
│                         │
│                         │
│                         │
│                  [LOGO] │ ← Just logo
└─────────────────────────┘
```

## 📐 Logo Specifications

### Recommended Dimensions
- **Width:** 150-200px
- **Height:** 150-200px (or proportional)
- **Format:** PNG with transparency
- **Resolution:** High-res (at least 300x300)

### Your Logo Specifically
Your orange sunrise burst logo works perfectly!
- Circular shape fits well
- Orange color matches brand
- Transparent background ideal

## 🔧 File Structure

```
bd-news-bot/
├── assets/
│   ├── scrollup_logo.png      ← Your main logo
│   └── scrollup_logo_white.png ← Optional: white version for dark backgrounds
├── config.py                   ← Logo settings here
├── image_generator_scrollup.py ← Uses the logo
└── generated_posts/            ← Output with your logo
```

## 🎯 How It Works

### Automatic Logo Detection

The bot checks:
1. **Does `assets/scrollup_logo.png` exist?**
   - ✅ YES → Use your actual logo
   - ❌ NO → Use text + orange dot (current)

2. **Logo Placement:**
   - Resizes to configured width
   - Maintains aspect ratio
   - Places in configured position
   - Adds shadow on photo backgrounds

### Smart Fallback

If logo file is missing or broken:
- Bot automatically uses text-based branding
- No crashes or errors
- Still looks professional

## 🖼️ Logo on Different Backgrounds

### White Background Posts
```
Your logo → Placed as-is
           (transparent background shows white)
```

### Black Background Posts
```
Your logo → Placed as-is
           (orange stands out on black)
```

### Photo Background Posts
```
Your logo → Placed with subtle shadow
           (ensures visibility on any photo)
```

## ✅ Quality Checklist

Before using your logo:
- [ ] PNG format (with transparency if possible)
- [ ] High resolution (300x300+ pixels)
- [ ] Named exactly: `scrollup_logo.png`
- [ ] Placed in `assets/` folder
- [ ] Logo looks clear at 150px width
- [ ] Works on both light and dark backgrounds

## 🚀 Quick Test

After adding your logo:

```bash
cd bd-news-bot

# Test with sample post
python3 -c "
from image_generator_scrollup import ScrollUpImageGenerator

gen = ScrollUpImageGenerator()
test_story = {
    'highlight': 'Test Post With Your Logo',
    'category': 'test',
    'sources': ['Test']
}

img = gen.generate_post_image(test_story, 'instagram')
print(f'Generated: {img}')
print('Check if your logo appears!')
"
```

Open the generated image - **your logo should be there!**

## 🎨 Advanced: Multiple Logo Versions

You can have different logo versions:

### Light Logo (for dark backgrounds)
```python
# In image_generator_scrollup.py, update:
if use_dark_background:
    LOGO_PATH = 'assets/scrollup_logo_white.png'
else:
    LOGO_PATH = 'assets/scrollup_logo.png'
```

### Small Logo (for compact spaces)
```python
# Different sizes for different platforms
if platform == 'instagram':
    LOGO_WIDTH = 150
else:  # facebook
    LOGO_WIDTH = 120
```

## 🐛 Troubleshooting

### Logo Not Showing?

**Check 1: File exists?**
```bash
ls -la assets/scrollup_logo.png
# Should show the file
```

**Check 2: File name correct?**
```bash
# Must be EXACTLY: scrollup_logo.png
# Not: ScrollUp_Logo.PNG or scrollup-logo.png
```

**Check 3: Run test**
```bash
python3 -c "
import os
from config import LOGO_PATH
print(f'Logo path: {LOGO_PATH}')
print(f'Logo exists: {os.path.exists(LOGO_PATH)}')
"
```

### Logo Too Big/Small?

Edit `config.py`:
```python
LOGO_WIDTH = 120  # Try different values: 100, 150, 200
```

### Logo In Wrong Position?

Edit `config.py`:
```python
LOGO_POSITION = 'bottom-right'  # Change to your preference
```

### Logo Not Transparent?

If your logo has a white box around it:
1. Open in photo editor (Photoshop, GIMP, Canva)
2. Remove background
3. Export as PNG with transparency
4. Replace file

## 📊 Before & After

### Without Logo (Current)
```
ScrollUp Today ●  ← Text + orange dot
```

### With Your Logo (After adding file)
```
ScrollUp Today [🌅]  ← Text + your actual sunrise logo!
```

## 💡 Pro Tips

1. **Export from Instagram**
   - Go to your Instagram profile
   - Download profile picture
   - Use as logo

2. **Match Your Posts**
   - Look at your existing posts
   - See logo size/position
   - Configure bot to match

3. **Test on Both Backgrounds**
   - Generate white background post
   - Generate black background post
   - Check logo visibility on both

4. **Keep Logo Simple**
   - Logo should be recognizable at small sizes
   - Avoid thin details
   - High contrast colors work best

## 🎯 What You'll Get

After adding your logo:

✅ **Every post** will have your actual logo  
✅ **Consistent branding** across all content  
✅ **Professional look** matching your manual posts  
✅ **Automatic placement** - no manual work needed  
✅ **Smart scaling** for different platforms  
✅ **Shadow on photos** for visibility  

## 📞 Need Help?

**Can't find assets folder?**
```bash
cd bd-news-bot
mkdir assets
echo "Folder created!"
```

**Wrong file format?**
- Convert to PNG online: convertio.co
- Or use any image editor

**Logo file corrupted?**
```bash
# Test if file is valid
file assets/scrollup_logo.png
# Should say: PNG image data
```

## 🎉 You're Done!

Once your logo is in `assets/scrollup_logo.png`:
1. ✅ Bot automatically uses it
2. ✅ No code changes needed
3. ✅ Appears on all posts
4. ✅ Professional branding

Just run:
```bash
python main.py
```

And your logo will be on every generated post! 🎨

---

**Remember:** File must be named exactly `scrollup_logo.png` and placed in `assets/` folder.
