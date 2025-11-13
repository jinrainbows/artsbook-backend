from flask import Flask, jsonify, request
import requests
from firebase_setup import database_ref
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return jsonify({"message": "Hello World from backend"})

#api for books
@app.route("/api/books")
def get_books():
    query = request.args.get("query", "harry potter")
    url = f"https://openlibrary.org/search.json?q={query}"
    res = requests.get(url)

    if res.status_code != 200:
        return jsonify({"error": "Failed to fetch books"}), 500

    data = res.json()
    books = [
        {
            "title": b.get("title"),
            "author": b.get("author_name", ["Unknown"])[0],
            "thumbnail": f"http://covers.openlibrary.org/b/id/{b['cover_i']}-M.jpg" if b.get("cover_i") else None
        }
        for b in data.get("docs", [])[:5]
    ]
    return jsonify({"results": books})

#api for movies and tv
@app.route("/api/movies")
def get_movies():
    query = request.args.get("query", "inception")
    api_key = "1f655943c2cbd205457f62599e088978"
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}"

    res = requests.get(url)
    if res.status_code != 200:
        return jsonify({"error": "Failed to fetch movies"}), 500

    data = res.json()
    movies = [
        {
            "title": m.get("title"),
            "thumbnail": f"https://image.tmdb.org/t/p/w500{m['poster_path']}" if m.get("poster_path") else None,
        }
        for m in data.get("results", [])[:5]
    ]
    return jsonify({"results": movies})


#write to database
@app.route("/api/reviews", methods=["POST"])
def post_review():
    data = request.get_json()
    username = data.get("username")
    content = data.get("content")

    if not username or not content:
        return jsonify({"error": "Missing username or content"}), 400

    review = {"username": username, "content": content}
    new_ref = database_ref.child("reviews").push(review)
    return jsonify({"message": "Review added", "id": new_ref.key, "review": review}), 201

#read from database
@app.route("/api/reviews", methods=["GET"])
def get_reviews():
    reviews = database_ref.child("reviews").get() or {}
    return jsonify(reviews)