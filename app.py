from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# 🧠 Memory
last_movie = None

# 🎬 Load Movie DB from txt file
db_path = os.path.join(os.path.dirname(__file__), 'movie_db.txt')
with open(db_path, 'r') as f:
    db_content = f.read()
    exec(db_content, globals())

# 🔍 Find movie
def find_movie(user_input):
    user_input = user_input.lower()
    for key in movie_db:
        if key in user_input:
            return movie_db[key]
    return None

# 🎯 Genre search
def recommend_by_genre(user_input):
    genres = ["action", "drama", "sci-fi"]

    for g in genres:
        if g in user_input:
            return [m for m in movie_db.values() if g.lower() in m["genre"].lower()]
    return None

# 🎭 Actor search
def movies_by_actor(user_input):
    results = []
    for m in movie_db.values():
        if any(actor.lower() in user_input for actor in m["actors"].lower().split(", ")):
            results.append(m)
    return results if results else None

# 🎬 Director search
def movies_by_director(user_input):
    results = []
    for m in movie_db.values():
        if m["director"].lower() in user_input:
            results.append(m)
    return results if results else None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global last_movie

    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"type": "text", "message": "⚠️ No message received"})

    user_message = data["message"].lower()

    # 🎬 Movie search
    movie = find_movie(user_message)
    if movie:
        last_movie = movie

        rating = float(movie["rating"])
        review = "🔥 Blockbuster! Must Watch!" if rating >= 8 else "👍 Good movie!"

        return jsonify({
            "type": "movie",
            "title": movie["title"],
            "year": movie["year"],
            "rating": movie["rating"],
            "actors": movie["actors"],
            "director": movie["director"],
            "plot": movie["plot"],
            "poster": movie["poster"],
            "trailer": movie.get("trailer", ""),
            "review": review
        })

    # 🎯 Genre
    genre_movies = recommend_by_genre(user_message)
    if genre_movies:
        return jsonify({"type": "movies", "movies": genre_movies})

    # 🎭 Actor
    actor_movies = movies_by_actor(user_message)
    if actor_movies:
        return jsonify({"type": "movies", "movies": actor_movies})

    # 🎬 Director
    director_movies = movies_by_director(user_message)
    if director_movies:
        return jsonify({"type": "movies", "movies": director_movies})

    # 🧠 MEMORY RESPONSES
    if last_movie:
        if "cast" in user_message:
            return jsonify({
                "type": "text",
                "message": f"🎭 Cast of {last_movie['title']}: {last_movie['actors']}"
            })

        if "director" in user_message:
            return jsonify({
                "type": "text",
                "message": f"🎬 Director of {last_movie['title']}: {last_movie['director']}"
            })

        if "rating" in user_message:
            return jsonify({
                "type": "text",
                "message": f"⭐ {last_movie['title']} rating is {last_movie['rating']}"
            })

        if "good" in user_message:
            return jsonify({
                "type": "text",
                "message": f"👍 {last_movie['title']} is worth watching!"
            })
        
        if "plot" in user_message:
            return jsonify({
                "type": "text",
                "message": f"🎬 Plot of {last_movie['title']}: {last_movie['plot']}"
            })

    return jsonify({
        "type": "text",
        "message": "🤖 Ask about movies, genres, actors, or directors!"
    })

if __name__ == "__main__":
    app.run(debug=True)