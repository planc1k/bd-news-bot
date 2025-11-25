import { useState, useEffect } from 'react';
import Head from 'next/head';

export default function Home() {
  const [posts, setPosts] = useState([]);
  const [stats, setStats] = useState({ total: 0, today: 0, sources: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      const response = await fetch('/api/posts');
      const data = await response.json();
      setPosts(data.posts || []);
      setStats(data.stats || { total: 0, today: 0, sources: [] });
      setLoading(false);
    } catch (error) {
      console.error('Error fetching posts:', error);
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>Bangladesh News Bot - Automated News Feed</title>
        <meta name="description" content="Automated Bangladeshi news aggregator" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="min-h-screen bg-gradient-to-b from-[#1A1A2E] to-[#43435D]">
        {/* Header */}
        <header className="border-b border-gray-700/50 backdrop-blur-sm bg-[#1A1A2E]/80 sticky top-0 z-50">
          <div className="container mx-auto px-4 py-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-white flex items-center gap-3">
                  <span className="text-4xl">🤖</span>
                  Bangladesh News Bot
                </h1>
                <p className="text-gray-400 mt-1">
                  Automated AI-powered news aggregation
                </p>
              </div>
              <button
                onClick={fetchPosts}
                className="px-4 py-2 bg-[#4ECDC4] text-white rounded-lg hover:bg-[#3DB8B0] transition-colors flex items-center gap-2"
              >
                <span>🔄</span> Refresh
              </button>
            </div>
          </div>
        </header>

        {/* Stats Bar */}
        <div className="bg-[#1A1A2E]/60 backdrop-blur-sm border-b border-gray-700/50">
          <div className="container mx-auto px-4 py-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-gradient-to-r from-[#FF6B6B]/20 to-[#FF6B6B]/10 rounded-lg p-4 border border-[#FF6B6B]/30">
                <div className="text-gray-400 text-sm">Total Posts</div>
                <div className="text-2xl font-bold text-white mt-1">{stats.total}</div>
              </div>
              <div className="bg-gradient-to-r from-[#4ECDC4]/20 to-[#4ECDC4]/10 rounded-lg p-4 border border-[#4ECDC4]/30">
                <div className="text-gray-400 text-sm">Posted Today</div>
                <div className="text-2xl font-bold text-white mt-1">{stats.today}</div>
              </div>
              <div className="bg-gradient-to-r from-[#FFE66D]/20 to-[#FFE66D]/10 rounded-lg p-4 border border-[#FFE66D]/30">
                <div className="text-gray-400 text-sm">News Sources</div>
                <div className="text-2xl font-bold text-white mt-1">{stats.sources.length}</div>
              </div>
            </div>
          </div>
        </div>

        {/* Posts Feed */}
        <div className="container mx-auto px-4 py-8">
          {loading ? (
            <div className="text-center py-20">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-[#4ECDC4] border-t-transparent"></div>
              <p className="text-gray-400 mt-4">Loading posts...</p>
            </div>
          ) : posts.length === 0 ? (
            <div className="text-center py-20">
              <div className="text-6xl mb-4">📰</div>
              <h2 className="text-2xl font-bold text-white mb-2">No Posts Yet</h2>
              <p className="text-gray-400">
                Run the bot to generate your first post!
              </p>
              <code className="block mt-4 bg-[#1A1A2E] text-[#4ECDC4] px-4 py-2 rounded">
                python main.py
              </code>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {posts.map((post, index) => (
                <article
                  key={index}
                  className="bg-[#1A1A2E]/60 backdrop-blur-sm rounded-xl overflow-hidden border border-gray-700/50 hover:border-[#4ECDC4]/50 transition-all hover:scale-[1.02]"
                >
                  {/* Image */}
                  {post.image && (
                    <div className="aspect-square bg-gray-800">
                      <img
                        src={post.image}
                        alt={post.title}
                        className="w-full h-full object-cover"
                      />
                    </div>
                  )}

                  {/* Content */}
                  <div className="p-5">
                    {/* Category Badge */}
                    <span className="inline-block px-3 py-1 bg-[#FFE66D] text-[#1A1A2E] text-xs font-bold rounded-full mb-3">
                      {post.category?.toUpperCase() || 'NEWS'}
                    </span>

                    {/* Title */}
                    <h3 className="text-xl font-bold text-white mb-2 line-clamp-2">
                      {post.title}
                    </h3>

                    {/* Summary */}
                    <p className="text-gray-400 text-sm mb-4 line-clamp-3">
                      {post.summary}
                    </p>

                    {/* Meta */}
                    <div className="flex items-center justify-between text-xs text-gray-500">
                      <div className="flex items-center gap-2">
                        <span>📰</span>
                        <span>{post.sources?.join(', ') || 'Unknown'}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span>🕐</span>
                        <span>{new Date(post.posted_at).toLocaleDateString()}</span>
                      </div>
                    </div>

                    {/* Hashtags */}
                    {post.hashtags && (
                      <div className="mt-3 text-xs text-[#4ECDC4]">
                        {post.hashtags}
                      </div>
                    )}
                  </div>
                </article>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <footer className="border-t border-gray-700/50 mt-20">
          <div className="container mx-auto px-4 py-8 text-center text-gray-400 text-sm">
            <p>
              🤖 Powered by Groq AI • Built with Next.js • Made for Bangladesh
            </p>
            <p className="mt-2">
              Automated news aggregation from {stats.sources.length}+ Bangladeshi sources
            </p>
          </div>
        </footer>
      </main>
    </>
  );
}
