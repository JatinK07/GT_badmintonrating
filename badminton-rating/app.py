from flask import Flask, request, redirect, render_template
from models.player import Player
from services.rating_system import handle_singles, handle_doubles
from utils.storage import load_players, save_players, load_matches, save_matches
import os

app = Flask(__name__)

DATA_DIR = "badminton-rating/data"
PLAYERS_FILE = os.path.join(DATA_DIR, "players.json")
MATCHES_FILE = os.path.join(DATA_DIR, "match_history.json")

players = load_players(PLAYERS_FILE)
matches = load_matches(MATCHES_FILE)

@app.route("/")
def index():
    ranked = sorted(players.values(), key=lambda p: p.rating, reverse=True)
    return render_template("index.html", players=ranked)

@app.route("/add_player", methods=["GET", "POST"])
def add_player():
    if request.method == "POST":
        player_id = request.form["id"]
        name = request.form["name"]
        city = request.form["city"]
        players[player_id] = Player(player_id, name, city)
        save_players(PLAYERS_FILE, players)
        return redirect("/")
    return render_template("add_player.html")

@app.route("/record_match", methods=["GET", "POST"])
def record_match():
    if request.method == "POST":
        match_type = request.form["match_type"]
        winner = request.form["winner"]

        if match_type == "singles":
            a = request.form["a"]
            b = request.form["b"]
            handle_singles(players[a], players[b], winner)
            matches.append({"type": "singles", "A": a, "B": b, "winner": winner})
        elif match_type == "doubles":
            a1 = request.form["a1"]
            a2 = request.form["a2"]
            b1 = request.form["b1"]
            b2 = request.form["b2"]
            handle_doubles([players[a1], players[a2]], [players[b1], players[b2]], winner)
            matches.append({"type": "doubles", "A": [a1, a2], "B": [b1, b2], "winner": winner})
        save_players(PLAYERS_FILE, players)
        save_matches(MATCHES_FILE, matches)
        return redirect("/")
    return render_template("record_match.html", players=players)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)