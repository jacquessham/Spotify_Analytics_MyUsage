import json


f = open('../../../../Spotify_Data/Spotify_Jacques_full_until2023Q2/Streaming_History_Audio_2023_7.json','r')
print(json.dumps(json.load(f)[0], indent=4))
