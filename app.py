from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 🧠 Memory
last_movie = None

# 🎬 Movie DB
movie_db = {
    "inception": {
        "title": "Inception",
        "year": "2010",
        "rating": "8.8",
        "actors": "Leonardo DiCaprio, Joseph Gordon-Levitt",
        "director": "Christopher Nolan",
        "plot": "A thief enters dreams to steal secrets.",
        "poster": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRyuWmayVBvqjd1MxTKpRgauq2cCtUzb7Q9QvaFTkAuxAU_EYMoCE3wBuJeftxIzf0grreIw&s=10",
        "genre": "Sci-Fi",
        "trailer": "https://www.youtube.com/embed/YoHD9XEInc0"
    },

    "interstellar": {
        "title": "Interstellar",
        "year": "2014",
        "rating": "8.6",
        "actors": "Matthew McConaughey, Anne Hathaway",
        "director": "Christopher Nolan",
        "plot": "A team travels through a wormhole to save humanity.",
        "poster": "https://m.media-amazon.com/images/I/71yHjHcU7XL._AC_SY679_.jpg",
        "genre": "Sci-Fi",
        "trailer": "https://www.youtube.com/embed/zSWdZVtXT7E"
    },

    "avatar": {
        "title": "Avatar",
        "year": "2009",
        "rating": "7.9",
        "actors": "Sam Worthington, Zoe Saldana",
        "director": "James Cameron",
        "plot": "A marine explores an alien world called Pandora.",
        "poster": "https://m.media-amazon.com/images/I/41kTVLeW1CL._AC_.jpg",
        "genre": "Sci-Fi",
        "trailer": "https://www.youtube.com/embed/5PSNL1qE6VY"
    },

    "titanic": {
        "title": "Titanic",
        "year": "1997",
        "rating": "7.9",
        "actors": "Leonardo DiCaprio, Kate Winslet",
        "director": "James Cameron",
        "plot": "A love story aboard the ill-fated Titanic ship.",
        "poster": "https://m.media-amazon.com/images/I/71yHjHcU7XL._AC_SY679_.jpg",
        "genre": "Romance",
        "trailer": "https://www.youtube.com/embed/kVrqfYjkTdQ"
    },

    "joker": {
        "title": "Joker",
        "year": "2019",
        "rating": "8.4",
        "actors": "Joaquin Phoenix",
        "director": "Todd Phillips",
        "plot": "A man descends into madness and becomes Joker.",
        "poster": "https://m.media-amazon.com/images/I/71z2m5W5ZxL._AC_SY679_.jpg",
        "genre": "Drama",
        "trailer": "https://www.youtube.com/embed/zAGVQLHvwOY"
    },

    "avengers_endgame": {
        "title": "Avengers: Endgame",
        "year": "2019",
        "rating": "8.4",
        "actors": "Robert Downey Jr., Chris Evans",
        "director": "Anthony Russo",
        "plot": "Heroes unite to undo Thanos' snap.",
        "poster": "https://m.media-amazon.com/images/I/81ExhpBEbHL._AC_SY679_.jpg",
        "genre": "Action",
        "trailer": "https://www.youtube.com/embed/TcMBFSGVi1c"
    },

    "vikram": {
        "title": "Vikram",
        "year": "2022",
        "rating": "8.3",
        "actors": "Kamal Haasan, Vijay Sethupathi",
        "director": "Lokesh Kanagaraj",
        "plot": "A special agent uncovers a drug syndicate.",
        "poster": "https://m.media-amazon.com/images/I/81uY6v8h6bL._AC_SY679_.jpg",
        "genre": "Action",
        "trailer": "https://www.youtube.com/embed/OKBMCL-frPU"
    },

    "master": {
        "title": "Master",
        "year": "2021",
        "rating": "7.3",
        "actors": "Vijay, Vijay Sethupathi",
        "director": "Lokesh Kanagaraj",
        "plot": "A professor clashes with a ruthless gangster.",
        "poster": "https://m.media-amazon.com/images/I/71XxL9sXEdL._AC_SY679_.jpg",
        "genre": "Action",
        "trailer": "https://www.youtube.com/embed/UTiXQcrLlv4"
    },

    "leo": {
        "title": "Leo",
        "year": "2023",
        "rating": "7.2",
        "actors": "Vijay, Trisha",
        "director": "Lokesh Kanagaraj",
        "plot": "A cafe owner hides a violent past.",
        "poster": "https://m.media-amazon.com/images/I/71k0z9pX1nL._AC_SY679_.jpg",
        "genre": "Action",
        "trailer": "https://www.youtube.com/embed/Po3jStA673E"
    },

    "jailer": {
        "title": "Jailer",
        "year": "2023",
        "rating": "7.1",
        "actors": "Rajinikanth, Vinayakan",
        "director": "Nelson",
        "plot": "A retired jailer hunts criminals.",
        "poster": "https://m.media-amazon.com/images/I/71T5z1m7sML._AC_SY679_.jpg",
        "genre": "Action",
        "trailer": "https://www.youtube.com/embed/Y5BeWdODPqo"
    },

    "enthiran": {
        "title": "Enthiran",
        "year": "2010",
        "rating": "7.1",
        "actors": "Rajinikanth, Aishwarya Rai",
        "director": "Shankar",
        "plot": "A robot develops emotions and turns dangerous.",
        "poster": "https://m.media-amazon.com/images/I/61x6h7gTgXL._AC_SY679_.jpg",
        "genre": "Sci-Fi",
        "trailer": "https://www.youtube.com/embed/sY_F6issHsU"
    },

    "2.0": {
        "title": "2.0",
        "year": "2018",
        "rating": "6.1",
        "actors": "Rajinikanth, Akshay Kumar",
        "director": "Shankar",
        "plot": "A scientist battles a supernatural force.",
        "poster": "https://m.media-amazon.com/images/I/71ZDY57yTQL._AC_SY679_.jpg",
        "genre": "Sci-Fi",
        "trailer": "https://www.youtube.com/embed/GV3HUDMQ-F8"
    },

    "kaithi": {
        "title": "Kaithi",
        "year": "2019",
        "rating": "8.5",
        "actors": "Karthi",
        "director": "Lokesh Kanagaraj",
        "plot": "A prisoner helps police in one night mission.",
        "poster": "https://m.media-amazon.com/images/I/81c2kZrR4sL._AC_SY679_.jpg",
        "genre": "Action",
        "trailer": "https://www.youtube.com/embed/3gY1VZf1T8A"
    },

    "soorarai_pottru": {
        "title": "Soorarai Pottru",
        "year": "2020",
        "rating": "8.7",
        "actors": "Suriya",
        "director": "Sudha Kongara",
        "plot": "A man dreams of making air travel affordable.",
        "poster": "https://m.media-amazon.com/images/I/71t6Z+QZ3UL._AC_SY679_.jpg",
        "genre": "Drama",
        "trailer": "https://www.youtube.com/embed/fa_DIwRsa9o"
    },

    "doctor": {
        "title": "Doctor",
        "year": "2021",
        "rating": "7.5",
        "actors": "Sivakarthikeyan",
        "director": "Nelson",
        "plot": "A doctor rescues a kidnapped girl.",
        "poster": "https://m.media-amazon.com/images/I/71gqFh7XGCL._AC_SY679_.jpg",
        "genre": "Comedy",
        "trailer": "https://www.youtube.com/embed/0wC0kU9oQ2A"
    },

    "beast": {
        "title": "Beast",
        "year": "2022",
        "rating": "5.3",
        "actors": "Vijay, Pooja Hegde",
        "director": "Nelson",
        "plot": "A spy rescues hostages in a mall.",
        "poster": "https://m.media-amazon.com/images/I/71nQd9x6pLL._AC_SY679_.jpg",
        "genre": "Action",
        "trailer": "https://www.youtube.com/embed/0E1kVRRi6lk"
    },

    "the_dark_knight": {
        "title": "The Dark Knight",
        "year": "2008",
        "rating": "9.0",
        "actors": "Christian Bale, Heath Ledger",
        "director": "Christopher Nolan",
        "plot": "Batman faces the Joker in Gotham.",
        "poster": "https://m.media-amazon.com/images/I/51EbJjlT5dL._AC_.jpg",
        "genre": "Action",
        "trailer": "https://www.youtube.com/embed/EXeTwQWrcwY"
    },

    "oppenheimer": {
        "title": "Oppenheimer",
        "year": "2023",
        "rating": "8.5",
        "actors": "Cillian Murphy",
        "director": "Christopher Nolan",
        "plot": "Story of the atomic bomb creator.",
        "poster": "https://m.media-amazon.com/images/I/71xBLRBYOiL._AC_SY679_.jpg",
        "genre": "Biography",
        "trailer": "https://www.youtube.com/embed/uYPbbksJxIg"
    },

    "spiderman_no_way_home": {
        "title": "Spider-Man: No Way Home",
        "year": "2021",
        "rating": "8.2",
        "actors": "Tom Holland",
        "director": "Jon Watts",
        "plot": "Spider-Man faces villains from multiverse.",
        "poster": "https://m.media-amazon.com/images/I/81f8f8zQ0XL._AC_SY679_.jpg",
        "genre": "Action",
        "trailer": "https://www.youtube.com/embed/JfVOs4VSpmA"
    },

    "doctor_strange": {
        "title": "Doctor Strange",
        "year": "2016",
        "rating": "7.5",
        "actors": "Benedict Cumberbatch",
        "director": "Scott Derrickson",
        "plot": "A surgeon becomes a mystical hero.",
        "poster": "https://m.media-amazon.com/images/I/71jz8g7YqGL._AC_SY679_.jpg",
        "genre": "Fantasy",
        "trailer": "https://www.youtube.com/embed/HSzx-zryEgM"
    }
}

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