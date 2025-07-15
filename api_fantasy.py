from flask import Flask, request, jsonify
import fpl_optimizer  # your module with the existing code
import requests


app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Fantasy API is running!"})

# Endpoint to optimize team with given existing_team input
@app.route('/optimize', methods=['POST'])
def optimize():
    data = request.json

    # Expected JSON format:
    # {
    #   "existing_team": {
    #       "starting": {...},
    #       "bench": {...}
    #   }
    # }

    existing_team = data.get('existing_team', {})

    # Fetch and prepare data once on server start, or inside function as needed
    players = fpl_optimizer.fetch_fpl_data()
    if players is None:
        return jsonify({"error": "Failed to fetch FPL data"}), 500

    df = fpl_optimizer.prepare_player_data(players)
    df = fpl_optimizer.assign_price_brackets(df)
    df = fpl_optimizer.filter_top_players(df, top_n=10)

    # Run optimizer
    result = fpl_optimizer.complete_team(df, existing_team)
 
    if result is None:
        return jsonify({"error": "No optimal solution found"}), 400

    start_result, bench_result = result

    return jsonify({
        "starting": start_result,
        "bench": bench_result
    })

if __name__ == "__main__":
    app.run(debug=True)
