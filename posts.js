import fs from 'fs';
import path from 'path';

export default function handler(req, res) {
  try {
    // Path to the posted stories JSON file
    const postsFilePath = path.join(process.cwd(), '../posted_stories.json');
    
    // Check if file exists
    if (!fs.existsSync(postsFilePath)) {
      return res.status(200).json({
        posts: [],
        stats: {
          total: 0,
          today: 0,
          sources: []
        }
      });
    }

    // Read the posted stories
    const fileContent = fs.readFileSync(postsFilePath, 'utf8');
    const postedStories = JSON.parse(fileContent);

    // Convert to array format
    const posts = Object.entries(postedStories).map(([id, data]) => ({
      id,
      title: data.summary?.split('\n')[0] || 'Untitled',
      summary: data.summary || '',
      sources: data.sources || [],
      posted_at: data.posted_at,
      image: data.images?.instagram || data.images?.facebook || null,
      hashtags: extractHashtags(data.summary),
      category: detectCategory(data.summary)
    }));

    // Sort by posted date (newest first)
    posts.sort((a, b) => new Date(b.posted_at) - new Date(a.posted_at));

    // Calculate stats
    const today = new Date().toDateString();
    const stats = {
      total: posts.length,
      today: posts.filter(p => new Date(p.posted_at).toDateString() === today).length,
      sources: [...new Set(posts.flatMap(p => p.sources))]
    };

    res.status(200).json({ posts, stats });
  } catch (error) {
    console.error('API Error:', error);
    res.status(500).json({ error: 'Failed to fetch posts', posts: [], stats: { total: 0, today: 0, sources: [] } });
  }
}

function extractHashtags(text) {
  if (!text) return '';
  const hashtags = text.match(/#\w+/g);
  return hashtags ? hashtags.slice(0, 5).join(' ') : '';
}

function detectCategory(text) {
  if (!text) return 'general';
  const textLower = text.toLowerCase();
  
  if (textLower.includes('cricket') || textLower.includes('sport')) return 'sports';
  if (textLower.includes('tech') || textLower.includes('ai')) return 'technology';
  if (textLower.includes('film') || textLower.includes('celebrity')) return 'entertainment';
  if (textLower.includes('politics') || textLower.includes('government')) return 'politics';
  if (textLower.includes('business') || textLower.includes('economy')) return 'economy';
  
  return 'general';
}
