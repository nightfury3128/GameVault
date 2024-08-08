import os
import asyncio
import aiohttp
from quart import Quart, render_template, request, jsonify
import json

app = Quart(__name__)

# Load API key and base URL from config.json
def load_config():
    with open('config.json') as f:
        return json.load(f)

config = load_config()
API_KEY = config['API_KEY']
BASE_URL = config['BASE_URL']

async def get_game_info(session, title):
    url = f"{BASE_URL}/games"
    params = {
        'key': API_KEY,
        'search': title,
        'page_size': 5
    }
    async with session.get(url, params=params) as response:
        if response.status == 200:
            games = await response.json()
            return games.get('results', [])
        else:
            await handle_error(response)
    return None

async def get_game_details(session, game_id):
    url = f"{BASE_URL}/games/{game_id}"
    params = {
        'key': API_KEY,
    }
    async with session.get(url, params=params) as response:
        if response.status == 200:
            return await response.json()
        else:
            await handle_error(response)
    return None

async def handle_error(response):
    print(f"Error: {response.status}", await response.json())

def is_hidden(folder):
    return folder.startswith('.') or (os.name == 'nt' and bool(os.stat(folder).st_file_attributes & 2))

def scan_top_level_directories(dir1, dir2, skip_folder):
    directories_to_scan = [dir1, dir2]
    folder_names = []

    for directory in directories_to_scan:
        with os.scandir(directory) as entries:
            for entry in entries:
                if entry.is_dir() and entry.name != skip_folder and not is_hidden(entry.path):
                    folder_names.append(entry.name)
    
    return folder_names

def truncate_description(description):
    if '.' in description:
        return description.split('.')[0] + '.'
    return description

async def fetch_game_data(title, session):
    game_infos = await get_game_info(session, title)
    if game_infos:
        best_match = game_infos[0]
        game_details = await get_game_details(session, best_match['id'])
        if game_details:
            game_details['description_raw'] = truncate_description(game_details.get('description_raw', 'No description available.'))
            game_details['local_path'] = f"C:\\Games\\{game_details['name']}"
            return game_details
    return None

@app.route('/')
async def index():
    sort_by = request.args.get('sort_by', 'name')
    dir1 = 'E:\\'
    dir2 = 'E:\\SteamLibrary\\steamapps\\common'
    skip_folder = 'SteamLibrary'
    game_titles = scan_top_level_directories(dir1, dir2, skip_folder)
    games_data = []

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_game_data(title, session) for title in game_titles]
        games_data = await asyncio.gather(*tasks)

    # Filter out None values
    games_data = [game for game in games_data if game]

    if sort_by == 'name':
        games_data.sort(key=lambda x: x['name'])
    elif sort_by == 'genre':
        games_data.sort(key=lambda x: x['genres'][0]['name'] if x['genres'] else '')

    return await render_template('index.html', games=games_data, sort_by=sort_by)

@app.route('/game/<int:game_id>')
async def game_details(game_id):
    async with aiohttp.ClientSession() as session:
        game_details = await get_game_details(session, game_id)
        if game_details:
            game_details['description_raw'] = truncate_description(game_details.get('description_raw', 'No description available.'))
            game_details['local_path'] = f"C:\\Games\\{game_details['name']}"
            return await render_template('details.html', game=game_details)
    return 'Game not found', 404

if __name__ == '__main__':
    app.run(debug=True)
