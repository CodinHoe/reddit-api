from flask import Flask, jsonify
import praw
import os
import datetime

app = Flask(__name__)

reddit = praw.Reddit(
    client_id=os.environ.get("REDDIT_CLIENT_ID"),
    client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
    user_agent="myredditapp/0.1 by u/yourusername"
)
reddit.read_only = True

@app.route("/")
def home():
    return "✅ Flask Reddit API is live! Try /reddit_data or /subreddit/python"

@app.route("/subreddit/<name>")
def get_subreddit_data(name):
    try:
        subreddit = reddit.subreddit(name)

        # Time filtering
        now = datetime.datetime.utcnow()
        one_day_ago = now - datetime.timedelta(days=1)
        one_day_timestamp = one_day_ago.timestamp()

        post_count = 0
        total_comments = 0
        total_score = 0

        # Fetch up to 100 'new' posts and filter by timestamp
        for post in subreddit.new(limit=100):
            if post.created_utc >= one_day_timestamp:
                post_count += 1
                total_comments += post.num_comments
                total_score += post.score  # Karma

        avg_karma = total_score / post_count if post_count > 0 else 0

        return jsonify({
            "subreddit": name,
            "subscribers": subreddit.subscribers,
            "active_users": subreddit.accounts_active,
            "posts_per_day": post_count,
            "comments_per_day": total_comments,
            "avg_karma": round(avg_karma, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/reddit_data")
def reddit_data():
    return "Reddit API is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
