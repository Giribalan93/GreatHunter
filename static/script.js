function addTextMessage(text, className) {
    let chatBox = document.getElementById("chat-box");

    let msg = document.createElement("div");
    msg.className = "message " + className;
    msg.innerText = text;

    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function addMovieCard(data) {
    let chatBox = document.getElementById("chat-box");

    let poster = data.poster && data.poster !== "N/A"
        ? data.poster
        : "https://via.placeholder.com/120x180";

    let recHTML = "";
    if (data.recommendations && data.recommendations.length > 0) {
        recHTML = "<p><b>🎯 Recommended:</b> " + data.recommendations.join(", ") + "</p>";
    }

    let card = document.createElement("div");
    card.className = "movie-card";

  card.innerHTML = `
    <img src="${poster}" class="poster">
    <div class="movie-info">
        <h4>${data.title}</h4>
        <p>⭐ ${data.rating}</p>
    </div>
`;

card.onclick = () => openModal(data);

    chatBox.appendChild(card);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function showTyping() {
    let chatBox = document.getElementById("chat-box");

    let typing = document.createElement("div");
    typing.className = "message bot";
    typing.id = "typing";
    typing.innerText = "🎬 Thinking...";

    chatBox.appendChild(typing);
}

function removeTyping() {
    let typing = document.getElementById("typing");
    if (typing) typing.remove();
}

function sendMessage() {
    let input = document.getElementById("user-input");
    let message = input.value;

    

    if (message.trim() === "") return;

    addTextMessage(message, "user");

    // 🎬 Typing animation with delay
    showTyping();

    setTimeout(() => {
        fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        })
        .then(res => {
            if (!res.ok) {
                throw new Error(`Server error ${res.status}`);
            }
            return res.json();
        })
        .then(data => {
            removeTyping();

            if (!data || !data.type) {
                addTextMessage("⚠️ Invalid response from server.", "bot");
                return;
            }

            if (data.type === "movie") {
                addMovieCard(data);
            } else if (data.type === "movies") {
                addMovieList(data.movies);
            } else {
                addTextMessage(data.message || "No info found.", "bot");
            }
        })
        .catch(err => {
            removeTyping();
            console.error(err);
            addTextMessage("⚠️ Error loading movies: " + err.message, "bot");
        });
    }, 800); // delay for realism

    input.value = "";
}

function startVoice() {
    let recognition = new webkitSpeechRecognition();
    recognition.onresult = function(event) {
        document.getElementById("user-input").value =
            event.results[0][0].transcript;
    };
    recognition.start();
}

function addMovieList(movies) {
    let chatBox = document.getElementById("chat-box");

    let container = document.createElement("div");
    container.className = "movie-list";

    movies.forEach(movie => {

        // ✅ SAFE VALUES (prevents undefined)
        let title = movie.title || "No Title";
        let rating = movie.rating || "N/A";
        let year = movie.year || "";
        let poster = movie.poster || "https://via.placeholder.com/120x180";
        let card = document.createElement("div");
        card.className = "movie-card";

        card.innerHTML = `
            <img src="${poster}" class="poster">
            <div class="movie-info">
                <h4>${title}</h4>
                <p>⭐ ${rating}</p>
                <p>${year}</p>
            </div>
        `;

        // ✅ CLICK EVENT
        card.onclick = () => openModal(movie);

        container.appendChild(card);
    });

    chatBox.appendChild(container);
    chatBox.scrollTop = chatBox.scrollHeight;
}
function openModal(movie) {
    if (!movie || typeof movie !== "object") {
        
        addTextMessage("⚠️ Movie data is unavailable.", "bot");
        return;
    }

    document.getElementById("movieModal").style.display = "block";

    document.getElementById("modal-title").innerText =
        (movie.title || "Unknown") + (movie.year ? " (" + movie.year + ")" : "");

    document.getElementById("modal-rating").innerText = movie.rating || "N/A";
    document.getElementById("modal-actors").innerText = movie.actors || "N/A";
    document.getElementById("modal-director").innerText = movie.director || "N/A";
    document.getElementById("modal-plot").innerText = movie.plot || "Plot unavailable.";

    let trailerEl = document.getElementById("trailer");
    if (movie.trailer && movie.trailer !== "N/A") {
        trailerEl.src = movie.trailer;
        trailerEl.style.display = "block";
    } else {
        trailerEl.src = "";
        trailerEl.style.display = "none";
    }
}

function closeModal() {
    document.getElementById("movieModal").style.display = "none";
    document.getElementById("trailer").src = "";
}

// Add Enter key functionality to input field
document.getElementById("user-input").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});