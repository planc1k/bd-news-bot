# 🌐 Bangladesh News Bot - Website

A beautiful Next.js website that displays all your automated news posts in real-time.

## ✨ Features

- **Real-time Feed**: Shows all posted news stories
- **Beautiful Design**: Matches your bot's bold, modern aesthetic
- **Stats Dashboard**: Total posts, posts today, active sources
- **Responsive**: Works perfectly on desktop, tablet, and mobile
- **Auto-refresh**: One-click refresh to see latest posts
- **Category Badges**: Visual indicators for news categories
- **Image Display**: Shows generated graphics for each post
- **Source Attribution**: Credits original news sources
- **Hashtag Display**: Shows hashtags used in posts

## 🎨 Design

The website matches your bot's design style:
- Dark gradient background (#1A1A2E to #43435D)
- Vibrant accent colors (Red, Teal, Yellow)
- Modern card-based layout
- Smooth animations and transitions
- Custom scrollbar styling

## 🚀 Quick Start

### Install Dependencies

```bash
cd website
npm install
```

### Run Development Server

```bash
npm run dev
```

Open http://localhost:3000 in your browser.

### Build for Production

```bash
npm run build
npm start
```

## 📁 Structure

```
website/
├── pages/
│   ├── index.js          # Main homepage
│   ├── _app.js           # Next.js app wrapper
│   └── api/
│       └── posts.js      # API endpoint for posts
├── styles/
│   └── globals.css       # Global styles + Tailwind
├── public/               # Static assets
├── package.json          # Dependencies
├── next.config.js        # Next.js configuration
├── tailwind.config.js    # Tailwind CSS config
└── tsconfig.json         # TypeScript config
```

## 🔌 How It Works

1. **API Endpoint** (`/api/posts`):
   - Reads `posted_stories.json` from parent directory
   - Converts to array format
   - Calculates stats (total, today, sources)
   - Returns JSON data

2. **Frontend** (`pages/index.js`):
   - Fetches data from API endpoint
   - Displays posts in beautiful card layout
   - Shows stats dashboard
   - Handles loading and empty states

3. **Data Flow**:
   ```
   Bot posts → posted_stories.json → API endpoint → Website displays
   ```

## 🎯 API Response Format

```json
{
  "posts": [
    {
      "id": "abc123...",
      "title": "News headline",
      "summary": "Full summary text",
      "sources": ["daily_star", "bdnews24"],
      "posted_at": "2025-11-24T18:00:00Z",
      "image": "path/to/image.png",
      "hashtags": "#Bangladesh #News #Breaking",
      "category": "technology"
    }
  ],
  "stats": {
    "total": 25,
    "today": 5,
    "sources": ["daily_star", "bdnews24", "prothom_alo"]
  }
}
```

## 🎨 Customization

### Change Colors

Edit `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: '#FF6B6B',    // Your brand color
      secondary: '#4ECDC4',  // Accent color
      accent: '#FFE66D',     // Highlight color
      dark: '#1A1A2E',       // Background
    },
  },
}
```

### Modify Layout

Edit `pages/index.js`:
- Change grid columns: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`
- Adjust spacing: `gap-6`
- Update card styling: Modify the `article` component

### Add New Stats

Edit `pages/api/posts.js` to calculate additional statistics:

```javascript
const stats = {
  total: posts.length,
  today: todayPosts.length,
  thisWeek: weekPosts.length,  // Add this
  sources: uniqueSources,
  categories: uniqueCategories  // Add this
};
```

## 🌐 Deploy to Vercel

### Option 1: With Main Bot

If deploying the whole project:

```bash
# From project root
vercel deploy --prod
```

The website will be available at your Vercel domain.

### Option 2: Separate Deployment

Deploy just the website:

```bash
cd website
vercel deploy --prod
```

**Important**: Make sure `posted_stories.json` is accessible to the website.

## 📊 Serving Images

### Local Development

Images are served from `../generated_posts/` directory.

### Production

For production, you have two options:

1. **Static File Serving**: Put images in `public/posts/`
2. **CDN**: Upload images to Cloudinary, AWS S3, or similar
3. **Update Image Paths**: Modify API to return full URLs

Example with CDN:

```javascript
// In api/posts.js
image: data.images?.instagram 
  ? `https://your-cdn.com/posts/${data.images.instagram}`
  : null
```

## 🔧 Troubleshooting

**Posts not showing?**
- Check that `posted_stories.json` exists
- Verify path in `api/posts.js`
- Run the bot first: `python main.py`

**Images not loading?**
- Check image paths in `posted_stories.json`
- Verify images exist in `generated_posts/`
- Update Next.js image domains in `next.config.js`

**API errors?**
- Check console for error messages
- Verify JSON file is valid
- Check file permissions

**Styling issues?**
- Run `npm install` to ensure Tailwind is installed
- Check that `globals.css` is imported in `_app.js`
- Clear `.next` folder and rebuild

## 🎓 Tech Stack

- **Next.js 14**: React framework with SSR
- **Tailwind CSS**: Utility-first CSS framework
- **React 18**: UI library
- **Node.js**: Backend runtime

## ⚡ Performance

- Server-side rendering for fast initial load
- Image optimization with Next.js Image
- Automatic code splitting
- CSS purging in production
- Caching strategy for API calls

## 📱 Responsive Design

- Mobile: Single column layout
- Tablet: 2-column grid
- Desktop: 3-column grid
- Large screens: 3+ columns

## 🔐 Security

- API runs server-side only
- No sensitive data in client
- Environment variables for secrets
- CORS handled by Next.js

## 🆕 Future Enhancements

Potential features to add:
- Search functionality
- Filter by category/source
- Date range filtering
- Individual post pages
- Analytics dashboard
- Admin panel for approving posts
- Real-time updates with WebSockets
- Export posts to CSV
- Share buttons for social media

## 📚 Documentation

- [Next.js Docs](https://nextjs.org/docs)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [React Docs](https://react.dev)

## 🆘 Need Help?

1. Check Next.js logs: `npm run dev`
2. Inspect browser console for errors
3. Verify API endpoint: http://localhost:3000/api/posts
4. Check that bot has generated posts

---

**Built with ❤️ for Bangladesh**
