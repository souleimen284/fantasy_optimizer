from flask import Flask, request, jsonify, send_from_directory
import fpl_optimizer  # your module with the existing code
import requests
import os
import json

app = Flask(__name__, static_folder='frontend/build', static_url_path='')

@app.route("/", methods=["GET"])
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route('/all-players', methods=['GET'])
def all_players():
    try:
        df = fpl_optimizer.fetch_fpl_data()  # this returns a DataFrame

        # Add now_cost (price) to the selected columns
        players = df[["id", "web_name", "element_type", "team", "now_cost"]].to_dict(orient="records")

        return jsonify({"players": players})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


    
@app.route('/resolve-players', methods=['POST'])
def resolve_players():
    data = request.json
    player_names = data.get("player_names", [])

    elements = fpl_optimizer.fetch_fpl_data()
    if elements.empty:
        return jsonify({"error": "Could not fetch FPL data"}), 500

    # Hardcoded positions mapping
    positions = {
        1: "GK",
        2: "DEF",
        3: "MID",
        4: "FWD"
    }

    result = {}
    for name in player_names:
        matches = elements[elements["web_name"].str.lower().str.contains(name.lower())]
        if matches.empty:
            return jsonify({"error": f"Player '{name}' not found"}), 404

        player = matches.iloc[0]
        pos = positions.get(player["element_type"], "UNK")  # Fallback to 'UNK' if not found
        price = player["now_cost"] / 10.0
        bracket = fpl_optimizer.find_bracket(price)
        key = f"{pos} {bracket}"
        result[key] = result.get(key, 0) + 1

    return jsonify({"existing_team": result})




# Endpoint to optimize team with given existing_team input
@app.route('/optimize', methods=['POST'])
def optimize():
    data = request.json
    existing_team = data.get('existing_team', {})

    players = fpl_optimizer.fetch_fpl_data()
    if players is None:
        return jsonify({"error": "Failed to fetch FPL data"}), 500

    df = fpl_optimizer.prepare_player_data(players)
    df = fpl_optimizer.assign_price_brackets(df)
    df = fpl_optimizer.filter_top_players(df, top_n=10)

    result = fpl_optimizer.complete_team(df, existing_team)  # pass flat dict directly
    if result is None:
        return jsonify({"error": "No optimal solution found"}), 400

    start_result, bench_result = result
    return jsonify({
        "starting": start_result,
        "bench": bench_result
    })

# 🔁 Let Flask handle all other routes for React Router
@app.route('/<path:path>')
def serve_react_app(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.run(debug=True)
