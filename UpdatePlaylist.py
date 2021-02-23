import PlaylistUtilities

#Create song list and filter list
songList = PlaylistUtilities.createSongList()
filterList = open("Filters.txt", "r")

#Go through filter list and update all playlists
for filter in filterList:
    #Remove the \n from the filter
    filter = filter.rstrip("\n")

    #Update most recent playlist
    if (filter == 'Most Recent'):
        tracks = [item.id for item in songList[0:25]]

    #Update Clean songs playlist
    elif (filter == 'Clean Songs'):
        tracks = [item.id for item in songList if not item.explicit]

    #Update short, medium and long term favorites playlists
    elif ('_term' in filter):
        tracks = PlaylistUtilities.topTracks(filter)
        if ('short' in filter):
            filter = "Short Term Favorites"
        elif('medium' in filter):
            filter = "Medium Term Favorites"
        else:
            filter = "Long Term Favorites"


    #Update the yearly playlists
    elif (filter.isnumeric()):
        tracks = [item.id for item in songList if item.checkReleaseDate(filter)]

    #Update the artist playlists
    else:
        tracks = [item.id for item in songList if item.checkArtist(filter)]

    PlaylistUtilities.update(filter, tracks)
