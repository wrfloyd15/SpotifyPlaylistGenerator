# SpotifyPlaylistGenerator

This project uses the Spotipy library to automatically generate and update spotify playlists

To automatically create playlists, add an artist or year to The "Filters.txt" file and run the UpdatePlaylist.py script. This file can also include:
- "Most Recent", which generates a playlist containing the user's 25 most recently liked songs
- "short_term", "medium_term", or "long_term" which contain the user's 50 most frequently listened-to songs over a 6 weeks, 6 months, or all-time

The NewMusic.py script automatically searches through Spotify's "New Music Friday" and "Release Radar" playlists and creates a new playlist for the user containing songs from those playlists by artists that they have already liked songs from.

The generateSpreadsheet.py and LikedSongsGraph.py scripts provide the user with additional information about their library. generateSpreadsheet.py creates a spreadsheet containing songs from the user's library as well as additional information about each song, such as artist, release date, and popularity. LikedSongsGraph.py shows the size of a user's library over time.
