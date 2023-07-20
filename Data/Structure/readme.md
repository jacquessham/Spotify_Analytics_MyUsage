# Sturctures of the Source Data
This folder will explain the structures of the source data. Note that, the data structure of transformed data in the data lake should be found in the <b>(Coming soon...)</b> folder.

## Listening Records

### Last 12 Months Record
After you have requested the <b>Account Data</b> from Spotify (The one received in 5 days), you will receive a zip file contains the following:
<ul>
	<li>DuoNewFamily.json</li>
	<li>Payments.json</li>
	<li>FamilyPlan.json</li>
	<li>Playlist<b>N</b>.json, where N is the number and depends on the number records you have</li>
	<li>Follow.json</li>
	<li>Read_Me_First.pdf</li>
	<li>Userdata.json</li>
	<li>Identifiers.json</li>
	<li>SearchQueries.json</li>
	<li>YourLibrary.json</li>
	<li>Inferences.json</li>
	<li>StreamingHistory<b>N</b>.json, where N is the number and depends on the number records you have</li>
</ul>

#### Columns in StreamingHistoryN.json
For the sake of this project, we will only need StreamingHistory<b>N</b>.json. In these files, it only contains the following columns in JSON format:

<ul>
	<li>endTime: The time the track stopped Playing in UTC, the format is YYYY-MM-DD HH:MM. Same as <b>ts</b> in the Full Record dataset. </li>
	<li>artistName: The artist name of the song. Same as <b>master_metadata_album_artist_name</b> in the Full Record dataset. </li>
	<li>trackName: The name of the song/podcast. Same as <b>master_metadata_track _name</b> in the Full Record dataset</li>
	<li>msPlayed: How long did the song/podcast was played in milliseconds (ms). Same as <b></b> in the Full Record dataset</li>
</ul>


<br><br>
An example of the Last 12 Months Record row looks like this:

```
  },
  {
    "endTime" : "2023-04-29 06:37",
    "artistName" : "Hikaru Utada",
    "trackName" : "Automatic",
    "msPlayed" : 328600
  }
]
```

### Full Record
After you have requested the <b>Account Data</b> from Spotify (The one received in 30 days, Spotify refers it as <b>Extended Streaming History</b>), you will receive a zip file contains the following:
<ul>
	<li>ReadMeFirst_ExtendedStreamingHistory</li>
  <li>StreamingHistory<b>N</b>.json, where N is the number and depends on the number records you have</li>
</ul>
<br><br>
The zip file does not contain other files available in the Last 12 Months Record. However, the Streaming History files contain more columns in the Extended Streaming History. <b>It is preferred to upload the Full Record to the data lake!</b>

#### Columns in StreamingHistoryN.json
<br><br>
An example of the Full Record row looks like this:
```
{
    "ts": "2023-02-23T23:05:53Z",
    "username": "jacquessham",
    "platform": "ios",
    "ms_played": 321800,
    "conn_country": "US",
    "ip_addr_decrypted": "Some IP Address",
    "user_agent_decrypted": "unknown",
    "master_metadata_track_name": "Another Chance",
    "master_metadata_album_artist_name": "Hikaru Utada",
    "master_metadata_album_album_name": "First Love",
    "spotify_track_uri": "spotify:track:0kYk4wjotkjhLVV7kqh5oA",
    "episode_name": null,
    "episode_show_name": null,
    "spotify_episode_uri": null,
    "reason_start": "trackdone",
    "reason_end": "trackdone",
    "shuffle": false,
    "skipped": false,
    "offline": false,
    "offline_timestamp": 1677193232,
    "incognito_mode": false
}
```

## Scripts
### Explore_datastructure.py
This script allows you quickly have a glance of a row in the Full Record in a prettified JSON format. <b>Be sure to change your directory before executing!</b>