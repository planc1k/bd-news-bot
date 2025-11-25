from groq import Groq
from config import GROQ_API_KEY, POST_LANGUAGE, CATEGORY_HASHTAGS
import re

class AIProcessor:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = "llama-3.1-70b-versatile"  # Fast and good quality
    
    def process_story(self, story_group):
        """
        Process a group of articles about the same story
        Returns a dictionary with summary, category, hashtags, etc.
        """
        # Combine information from all articles in the group
        combined_info = self._combine_articles(story_group['articles'])
        
        # Generate summary
        summary = self._generate_summary(combined_info)
        
        # Determine category
        category = self._categorize_story(combined_info)
        
        # Generate hashtags
        hashtags = self._generate_hashtags(summary, category)
        
        # Extract key quote or statistic if available
        highlight = self._extract_highlight(combined_info)
        
        return {
            'summary': summary,
            'category': category,
            'hashtags': hashtags,
            'highlight': highlight,
            'sources': story_group['sources'],
            'importance_score': story_group['importance_score'],
            'original_articles': story_group['articles']
        }
    
    def _combine_articles(self, articles):
        """Combine multiple articles into one text for processing"""
        combined = ""
        for article in articles:
            combined += f"Source: {article['source']}\n"
            combined += f"Title: {article['title']}\n"
            combined += f"Description: {article.get('description', '')}\n\n"
        return combined
    
    def _generate_summary(self, text):
        """Generate an engaging social media summary"""
        
        language_instruction = ""
        if POST_LANGUAGE == 'bengali':
            language_instruction = "Write the summary in Bengali language."
        elif POST_LANGUAGE == 'english':
            language_instruction = "Write the summary in English language."
        else:
            language_instruction = "Write the summary in both English and Bengali."
        
        prompt = f"""You are a social media content creator for Bangladeshi news. 
Create a short, engaging summary of this news story for Instagram/Facebook.

Requirements:
- Maximum 150 words
- Bold, attention-grabbing opening
- Include key facts and why it matters
- Use emojis strategically (1-2 max)
- Conversational but professional tone
- {language_instruction}

News Articles:
{text}

Summary:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a skilled social media content creator specializing in Bangladeshi news."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            summary = response.choices[0].message.content.strip()
            return summary
        
        except Exception as e:
            print(f"AI Error: {str(e)}")
            # Fallback to first article title and description
            return text.split('\n')[1].replace('Title: ', '')
    
    def _categorize_story(self, text):
        """Determine the category of the story"""
        text_lower = text.lower()
        
        categories = {
            'politics': ['government', 'minister', 'parliament', 'election', 'policy', 'pm', 'president'],
            'entertainment': ['film', 'movie', 'actor', 'actress', 'music', 'singer', 'celebrity', 'bollywood'],
            'sports': ['cricket', 'football', 'match', 'player', 'team', 'tournament', 'champion'],
            'technology': ['tech', 'ai', 'digital', 'app', 'software', 'internet', 'smartphone'],
            'economy': ['business', 'economy', 'trade', 'market', 'bank', 'finance', 'investment']
        }
        
        scores = {}
        for category, keywords in categories.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[category] = score
        
        # Return category with highest score, or 'general' if no clear category
        max_category = max(scores, key=scores.get)
        return max_category if scores[max_category] > 0 else 'general'
    
    def _generate_hashtags(self, summary, category):
        """Generate relevant hashtags"""
        # Start with category-specific hashtags
        base_hashtags = CATEGORY_HASHTAGS.get(category, CATEGORY_HASHTAGS['general'])
        
        # Extract potential hashtag words from summary
        words = re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)*\b', summary)
        custom_hashtags = [f"#{word}" for word in words[:2]]
        
        # Combine
        all_hashtags = base_hashtags + ' ' + ' '.join(custom_hashtags)
        
        return all_hashtags
    
    def _extract_highlight(self, text):
        """Extract a key quote, number, or fact to highlight in the image"""
        
        prompt = f"""Extract ONE key fact, statistic, or quote from this news that would be eye-catching on a social media graphic.

Requirements:
- Maximum 15 words
- Should be impactful and surprising
- Can be a quote, number, or key fact
- Return ONLY the extracted text, nothing else

News:
{text[:1000]}

Key highlight:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=50
            )
            
            highlight = response.choices[0].message.content.strip()
            # Remove quotes if present
            highlight = highlight.strip('"').strip("'")
            return highlight
        
        except Exception as e:
            print(f"Highlight extraction error: {str(e)}")
            # Fallback: use the title
            title = text.split('\n')[1].replace('Title: ', '')
            return title[:80] if len(title) > 80 else title

# Quick test
if __name__ == "__main__":
    processor = AIProcessor()
    
    # Test with sample data
    test_story = {
        'articles': [
            {
                'source': 'daily_star',
                'title': 'Bangladesh Cricket Team Wins Against India',
                'description': 'In a thrilling match, Bangladesh defeated India by 5 wickets.',
                'language': 'english'
            }
        ],
        'sources': ['daily_star'],
        'importance_score': 1
    }
    
    result = processor.process_story(test_story)
    print("Summary:", result['summary'])
    print("Category:", result['category'])
    print("Hashtags:", result['hashtags'])
    print("Highlight:", result['highlight'])
