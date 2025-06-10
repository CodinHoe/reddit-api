from flask import Flask, jsonify
import praw
import os

app = Flask(__name__)

reddit = praw.Reddit(
    client_id=os.environ.get("REDDIT_CLIENT_ID"),
    client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
    user_agent="myredditapp/0.1 by u/yourusername"
)

@app.route("/subreddit/<name>")
def get_subreddit_data(name):
    try:
        subreddit = reddit.subreddit(name)
        return jsonify({
            "subreddit": name,
            "subscribers": subreddit.subscribers,
            "active_users": subreddit.accounts_active,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@app.route("/")
def home():
    return "✅ Flask Reddit API is live! Try /reddit_data or /subreddit/python"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
