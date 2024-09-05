from flask import Flask, render_template, request
import requests
import os 
app = Flask(__name__)

# Function to get game data from RAWG API
def get_game_data(game_name, api_key):
    url = f"https://api.rawg.io/api/games?key={api_key}&search={game_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            game = data['results'][0]
            # Extract additional details
            description = game.get('description', 'No description available')
            genres = ', '.join(genre['name'] for genre in game.get('genres', []))
            return {
                'name': game.get('name'),
                'release_date': game.get('released', 'N/A'),
                'metacritic': game.get('metacritic', 'N/A'),
                'background_image': game.get('background_image', ''),
                'description': description,
                'genres': genres
            }
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        directories = request.form['directories'].split(',')
        directories = [dir.strip() for dir in directories]
        api_key = "21f861ed6a5f404a87815e6ec55d88d3"  # Replace with your RAWG API key

        game_data_list = []
        for directory in directories:
            # Handle SteamLibrary or other directories
            if directory.endswith("SteamLibrary"):
                directory = os.path.join(directory, "steamapps", "common")

            if os.path.exists(directory) and os.path.isdir(directory):
                top_level_folders = [
                    name for name in os.listdir(directory)
                    if os.path.isdir(os.path.join(directory, name)) and not name.startswith('.')
                ]
                for folder in top_level_folders:
                    # Filter out hidden folders
                    folder_path = os.path.join(directory, folder)
                    if not folder.startswith('.'):
                        game_data = get_game_data(folder, api_key)
                        if game_data:
                            game_data['folder'] = folder
                            game_data_list.append(game_data)
                        else:
                            game_data_list.append({
                                'folder': folder,
                                'error': 'Game data not found'
                            })
            else:
                game_data_list.append({
                    'folder': directory,
                    'error': 'Directory does not exist or is not accessible'
                })

        return render_template('index.html', game_data_list=game_data_list)
    return render_template('index.html', game_data_list=None)

if __name__ == '__main__':
    app.run(debug=True)
