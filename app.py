from flask import Flask, request, jsonify, send_from_directory # Added send_from_directory
from flask_cors import CORS
import requests
import os
import re

# Configure the Flask app to serve static files from the React build directory
app = Flask(__name__, static_folder='frontend/build', static_url_path='/')
CORS(app)

# Function to get game data from RAWG API (remains unchanged)
def get_game_data(game_name, api_key):
    url = f"https://api.rawg.io/api/games?key={api_key}&search={game_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            game = data['results'][0]
            description_html = game.get('description', 'No description available')
            description_text = re.sub(r'<[^>]+>', '', description_html)
            genres_list = game.get('genres', [])
            genres = ', '.join(genre['name'] for genre in genres_list if 'name' in genre)
            return {
                'name': game.get('name'),
                'release_date': game.get('released', 'N/A'),
                'metacritic': game.get('metacritic', 'N/A'),
                'background_image': game.get('background_image', ''),
                'description': description_text,
                'genres': genres
            }
    return None

@app.route('/api/search_games', methods=['POST'])
def api_search_games():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    data = request.get_json()
    directories_str = data.get('directories')
    if not directories_str:
        return jsonify({"error": "Missing 'directories' field"}), 400
    directories = directories_str.split(',')
    directories = [dir.strip() for dir in directories]
    api_key = "21f861ed6a5f404a87815e6ec55d88d3"
    game_data_list = []
    for directory in directories:
        directory_to_scan = directory
        if directory.endswith("SteamLibrary"):
            directory_to_scan = os.path.join(directory, "steamapps", "common")

        if os.path.exists(directory_to_scan) and os.path.isdir(directory_to_scan):
            top_level_folders = [
                name for name in os.listdir(directory_to_scan)
                if os.path.isdir(os.path.join(directory_to_scan, name)) and not name.startswith('.')
            ]
            if not top_level_folders and (directory_to_scan == directory or os.path.basename(directory_to_scan) == "common"): # Path itself is a game folder
                 game_name_candidate = os.path.basename(directory)
                 game_data = get_game_data(game_name_candidate, api_key)
                 if game_data:
                     game_data['folder'] = game_name_candidate
                     game_data_list.append(game_data)
                 else:
                     game_data_list.append({
                        'folder': game_name_candidate,
                        'name': game_name_candidate,
                        'error': 'Game data not found or RAWG API error'
                    })
            else: # Process subfolders
                for folder in top_level_folders:
                    game_data = get_game_data(folder, api_key)
                    if game_data:
                        game_data['folder'] = folder
                        game_data_list.append(game_data)
                    else:
                        game_data_list.append({
                            'folder': folder,
                            'name': folder,
                            'error': 'Game data not found or RAWG API error'
                        })
        else:
            game_data_list.append({
                'folder': directory,
                'name': os.path.basename(directory),
                'error': 'Directory does not exist or is not accessible'
            })
    return jsonify(game_data_list)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
