# Sturctures of the Source Data
This folder will explain the structures of the source data. Note that, the data structure of transformed data in the data lake should be found in the [ELT](../ELT) folder.

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
	<li>msPlayed: How long did the song/podcast was played in milliseconds (ms). Same as <b>ms_played</b> in the Full Record dataset</li>
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

<br><br>
You may find the details in Spotify Data privacy <a href="https://support.spotify.com/us/article/understanding-my-data/">documentation page</a>.

### Full Record
After you have requested the <b>Account Data</b> from Spotify (The one received in 30 days, Spotify refers it as <b>Extended Streaming History</b>), you will receive a zip file contains the following:
<ul>
	<li>ReadMeFirst_ExtendedStreamingHistory</li>
  <li>StreamingHistory<b>N</b>.json, where N is the number and depends on the number records you have</li>
</ul>
<br><br>
The zip file does not contain other files available in the Last 12 Months Record. However, the Streaming History files contain more columns in the Extended Streaming History. <b>It is preferred to upload the Full Record to the data lake!</b>

#### Columns in StreamingHistory_Audio_(period).json
The full dataset zip file received from Spotify contains a handful of <i>StreamingHistory_Audio_(period).json</i>, where period stated the date interval of the records. Each record contains more information than <i>StreamingHistoryN.json</i>. Here are the columns could be found in each record:

<br><br>
<ul>
  <li>ts: The time the track stopped Playing in UTC, the format is YYYY-MM-DD HH:MM. Same as <b>endTime</b> in the Last 12 Months dataset. </li>
  <li>username: The Spotify username</li>
  <li>platform: Which platform the song was played, eg, iOS, Android, Chromecast</li>
  <li>ms_Played: How long did the song/podcast was played in milliseconds (ms). Same as <b>msPlayed</b> in the Last 12 Months dataset.</li>
  <li>conn_country: The location (country code) where the song was played</li>
  <li>ip_addr_decrypted: IP Address connected when the song was played</li>
  <li>user_agent_decrypted: User Agent when the songs was played, eg, browser like Firefox or Safair</li>
  <li>master_metadata_track _name: The name of the song/podcast. Same as <b>trackName</b> in the Last 12 Months dataset.</li> 
  <li>master_metadata_album_artist_name: The artist name of the song. Same as <b>artistName</b> in the Last 12 Months dataset. </li>
  <li>master_metadata_album_album_name: The album name the song belongs to. Null means the song do not assoicated with any album</li>
  <li>spotify_track_uri: Spotify Track URI to identify the unique music track</li>
  <li>episode_name: Podcast name</li>
  <li>episode_show_name: Show name of the podcast belongs to</li>
  <li>spotify_episode_uri: Spotify Track URI to identify the unique podcast track</li>
  <li>reason_start: The reason the song start, including: <i>Click Row</i>, <i>Forward Button</i>, <i>Play Button</i>, and <i>Track Done</i></li>
  <li>reason_end: The reason the song start, including: <i>End Play</i>, <i>Forward Button</i>,  and <i>Track Done</i></li>
  <li>shuffle: Whether the song is played under shuffle mode. True of False.</li>
  <li>skipped: Whether the song is skipped by the user to the next song. True or False.</li>
  <li>offline: Whether the song is played offline. True or False.</li>
  <li>offline_timestamp: <i>ts</i> while played offline, usually same as <i>ts</i></li>
  <li>incognito_mode: Whether the song is played in the incognito mode. True or False</li>

  
</ul>
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

You may find the details in Spotify Data privacy <a href="https://support.spotify.com/us/article/understanding-my-data/">documentation page</a>.

## Scripts
### Explore_datastructure.py
This script allows you quickly have a glance of a row in the Full Record in a prettified JSON format. <b>Be sure to change your directory before executing!</b>


## Reference
Spotify Data privacy <a href="https://support.spotify.com/us/article/understanding-my-data/">documentation page</a>