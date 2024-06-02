import spotipy
from spotipy.oauth2 import SpotifyOAuth
import csv

CLIENT_ID = '07a0800fd29f4f178958d2ed249b24c1'
CLIENT_SECRET = '3ffba6a360d943eca14a252927d738f4'
REDIRECT_URI = 'http://localhost:8080/'  # Must match the redirect URI set in Spotify Dashboard

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, 
                                               redirect_uri=REDIRECT_URI, scope='user-library-read'))
podcast_uri = 'spotify:show:6kd62V3OM9CqGAJci9JYV8'

# Retrieve all episode IDs
all_episode_ids = []

offset = 0
limit = 50

while True:
    results = sp.show_episodes(podcast_uri, limit=limit, offset=offset)
    episodes = results['items']
    
    if not episodes:
        break
    
    episode_ids = [episode['id'] for episode in episodes]
    all_episode_ids.extend(episode_ids)
    
    offset += limit
    
# Define CSV file path
csv_file_path = 'episode_4.csv'

# Write episode IDs to the CSV file
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Episode ID'])
    writer.writerows([[episode_id] for episode_id in all_episode_ids])


print(f"Episode IDs have been saved to {csv_file_path}")