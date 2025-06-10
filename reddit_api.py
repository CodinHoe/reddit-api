from flask import Flask, jsonify
import praw

app = Flask(__name__)

# Initialize Reddit client
reddit = praw.Reddit(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    user_agent='YourAppName'
)

@app.route("/subreddit/<name>")
def get_subreddit_data(name):
    try:
        subreddit = reddit.subreddit(name)
        return jsonify({
            "subreddit": name,
            "subscribers": subreddit.subscribers,
            "active_users": subreddit.accounts_active,
            # Add more stats here if needed
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Reddit API is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
