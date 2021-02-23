import PlaylistUtilities

#Initialize variables
relevantSongs = []
artistList = PlaylistUtilities.createArtistList()

#Go through New Music Friday and Release Radar to find relevant tracks
PlaylistUtilities.searchPlaylist("New Music Friday", relevantSongs, artistList)
PlaylistUtilities.searchPlaylist("Release Radar", relevantSongs, artistList)

#Add songs to the playlist if they contain a previously liked artist
PlaylistUtilities.update("New Music", relevantSongs)

'''
#New releases
releases = sp.new_releases(limit = 50)
for item in releases['albums']['items']:
    print(item['artists'])
'''
