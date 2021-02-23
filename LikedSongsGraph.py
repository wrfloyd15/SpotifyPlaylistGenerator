import PlaylistUtilities
import matplotlib.pyplot as plt

#Create the song lists and get the offsets
songList = PlaylistUtilities.createSongList()
finalDay = songList[0].day_offset       #Most recent day that you liked a song
songList.reverse()                      #List needs to be oldest to newest
offset = songList[0].day_offset         #First day that you liked a song
songOffsetsList = [song.day_offset - offset for song in songList]
librarySize = [0] * (1 + finalDay - offset)

#Go through the list of offsets and determine how many songs were liked each day
i = 0
total = 0
while (i <= finalDay - offset):
    librarySize[i] = songOffsetsList.count(i) + total
    total = librarySize[i]
    i += 1

#Create and display the plot
plt.plot(librarySize)
plt.show()
