import spotipy
import spotipy.util as util
from client_info import my_username, my_client_id, my_client_secret,scope
from datetime import date, datetime


token = util.prompt_for_user_token(my_username, scope, client_id=my_client_id,client_secret=my_client_secret,redirect_uri='http://localhost')
sp = spotipy.Spotify(auth=token)

#Holds information about a spotify track
class song:
    def __init__(self, item):
        self.date_added = item['added_at'][0:10]
        self.title = item['track']['name']
        self.artists = self.createArtistList(item['track']['artists'])
        self.release_date = item['track']['album']['release_date'][0:4]
        self.popularity = item['track']['popularity']
        self.id = item['track']['uri']
        self.explicit = item['track']['explicit']
        self.day_offset = self.get_day_offset(self.date_added)
    def createArtistList(self, artists):
        names = []
        for artist in artists:
            names.append(artist['name'])
        return names
    def checkArtist(self, artist):
        if (artist in self.artists):
            return True
        return False
    def checkReleaseDate(self, date):
        if (self.release_date == date):
            return True
        return False
    def get_day_offset(self, date):
        year = int(date[0:4])
        month = int(date[5:7])
        day = int(date[8:10])

        day_of_year = datetime(year, month, day).timetuple().tm_yday
        return day_of_year + (year - 2008)*365


#Generates and returns a list of song objects representing user's liked songs
def createSongList():
    songList = []
    count = 50
    i=0
    print("Searching liked songs...")
    while (count == 50):
        count = 0
        results = sp.current_user_saved_tracks(limit = 50, offset = 50*i)
        for item in results['items']:
            currentSong = song(item)
            songList.append(currentSong)
            count += 1
        i += 1
    print(f"Found {50*(i-1)+count} songs.")
    return songList

#Returns a list of all artists for user-liked songs
def createArtistList():
    artistList = []
    count = 50
    i=0
    print("Creating list of artists...")
    while (count == 50):
        count = 0;
        results = sp.current_user_saved_tracks(limit = 50, offset = 50*i)
        for item in results['items']:
            count += 1
            currentSong = song(item)
            if (currentSong.artists[0] not in artistList):
                artistList.append(currentSong.artists[0])
        i += 1
    print(f"Found {len(artistList)} artists.")
    return artistList

#Helper functions for update
def updatePlaylist(id, tracks):
    #replace songs from playlist
    if (len(tracks)>100):
        sp.user_playlist_replace_tracks(my_username, id, tracks[0:100])
        tracks = tracks[100:]
        while len(tracks) > 50:
            sp.user_playlist_add_tracks(my_username, id, tracks[0:50])
            tracks = tracks[50:]
    else:
        sp.user_playlist_replace_tracks(my_username, id, tracks)

    #Add date to the description
    today = date.today()
    currentDate = today.strftime("%B %d, %Y")
    sp.user_playlist_change_details(my_username, id, description=f"Updated on {currentDate}")
def createPlaylist(filter, tracks):
        #Add the date to the playlist
        today = date.today()
        currentDate = today.strftime("%B %d, %Y")
        description = f"Updated on {currentDate}"

        #Create the playlist
        playlist = sp.user_playlist_create(my_username, filter, public=False,description=description)
        id = getPlaylistID(filter)

        while len(tracks) > 50:
            sp.user_playlist_add_tracks(my_username, id, tracks[0:50])
            tracks = tracks[50:]
        sp.user_playlist_add_tracks(my_username, id, tracks)

#Returns the ID of the playlist with the specified name
def getPlaylistID(playlistName):
    #check that playlist exists
    playlists = sp.current_user_playlists(limit = 50, offset = 0)
    id = ''
    for item in playlists['items']:
        if item['name'].lower() == playlistName.lower():
            return item['id']

#Returns true if the user has a playlist with playlistName, false otherwise
def playlistExists(playlistName):
    #check that playlist exists
    playlists = sp.current_user_playlists(limit = 50, offset = 0)
    for item in playlists['items']:
        if item['name'].lower() == playlistName.lower():
            return True
    return False

#Creates a playlist with tracks or replaces existing playlist with tracks
def update(filter, tracks):
    if playlistExists(filter):
        print(f"Playlist {filter} exists. Updating... ")
        id = getPlaylistID(filter)
        updatePlaylist(id, tracks)
        print(f"Playlist {filter} updated. ")
    else:
        print(f"Playlist {filter} does not exist. Creating... ")
        createPlaylist(filter, tracks)
        print(f"{filter} playlist created. ")
    tracks.clear()

#Helper function for searchPlaylist
def checkArtists(ArtistList, song):
    for artist in song.artists:
        if artist in ArtistList:
            return True
    return False

#Searches playlistName for songs by artists in artistList and appends them to relevantSongs
def searchPlaylist(playlistName, relevantSongs, artistList):
        #Get tracks from the playlist that was passed in
        if (playlistExists(playlistName)):
            id = getPlaylistID(playlistName)
        tracks = sp.playlist_tracks(id)

        #Add tracks to the new playlist if the artist is a liked artist
        for item in tracks["items"]:
            if (item['track'] is not None):
                currentSong = song(item)
                if (currentSong.id not in relevantSongs and checkArtists(artistList, currentSong)):
                    relevantSongs.append(currentSong.id)

def topTracks(timeFrame):
    tracks = []
    results = sp.current_user_top_tracks(limit = 50, offset = 0, time_range=timeFrame)
    for item in results['items']:
        tracks.append(item['uri'])
    return tracks
