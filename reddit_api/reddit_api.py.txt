from flask import Flask, jsonify
import requests

app = Flask(__name__)

CLIENT_ID = 'A2yfynaJYdbYdtBLbgw-aA'
CLIENT_SECRET = 'VenDgxZ38Nr4shiZfz_Y5tPv37E33g'
USER_AGENT = 'REI Spreadsheet App'

def get_token():
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    headers = {"User-Agent": USER_AGENT}
    data = {"grant_type": "client_credentials"}
    res = requests.post("https://www.reddit.com/api/v1/access_token",
                        auth=auth, data=data, headers=headers)
    return res.json().get("access_token")

@app.route("/subreddit/<sub>")
def get_subreddit(sub):
    token = get_token()
    headers = {"Authorization": f"bearer {token}", "User-Agent": USER_AGENT}
    res = requests.get(f"https://oauth.reddit.com/r/{sub}/about", headers=headers)

    if res.status_code != 200:
        return jsonify({"error": res.status_code}), res.status_code

    data = res.json().get("data", {})
    return jsonify({
        "subscribers": data.get("subscribers"),
        "active_users": data.get("accounts_active"),
        "title": data.get("title"),
        "description": data.get("public_description")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
