#procentowy podział bazy danych 
def database_divide(number):
	fileTrain = open(str(number) + '_learn','w')

	for index in range(0, number*1000):
		fileTrain.write(data[index])
		fileTrain.write('\n')

	fileTrain.close()
	fileTest = open(str(number) + '_test','w')

	for index in range(number*1000, 100000):
		fileTest.write(data[index])
		fileTest.write('\n')

	fileTest.close() 

#generowanie listy wg średniej ocen filmów
def generateAverageList(movies_number):
    moviesDic = {}
    avgList = []
    for key in range(0, 1683):
        moviesDic[str(key)] = 0

    for line in open("u.data", "r"):
        lineTemp = str.split(line, "\t")
        moviesDic[lineTemp[1]] = round((moviesDic[lineTemp[1]] + int(lineTemp[2])) / 2, 2)
    sortedMovies = ((k, moviesDic[k]) for k in sorted(moviesDic, key=moviesDic.get, reverse=True))

    for key, value in sortedMovies:
        avgList.append(key)
        if len(avgList) >= movies_number:
            break
    fileAvg = open('moviesAverage','w')
    for movie in avgList:
    	fileAvg.write(movie)
    	fileAvg.write('\n')
    fileAvg.close()


#tworzenie listy po kategoriach
def partByCategory():
	temp = str.split(open("u.item", "r").read(), '\n')
	moviesCategory = []
	for i in range(1, 1683):
		moviesCategory.append([])

	for item in temp:
		line = str.split(item, '|')
		for x in range(0, 19):
			moviesCategory[int(line[0]) - 1].append(line[5+x])

	moviesList = []
	averageList = []
	for x in range(0, 19):
		moviesList.append([])
		averageList.append([])
	
	for genre in range(0, 19):
		movie_index = 1
		for item in moviesCategory:
			if(int(item[genre]) == 1):
				moviesList[genre].append(movie_index)
			movie_index	 += 1

	moviesDic = {}
	for key in range(0, 1683):
		moviesDic[str(key)] = 0

	for line in open("u.data", "r"):
		lineTemp = str.split(line, "\t")
		moviesDic[lineTemp[1]] = round((moviesDic[lineTemp[1]] + int(lineTemp[2])) / 2, 2)

	for genre in range(0,19):
		for item in moviesList[genre]:
			averageList[genre].append("%d %.2f" %(item, moviesDic[str(item)]))

	for genre in range(0, 19):
		fileCategory = open('movies' + str(genre), 'w')
		for movie in averageList[genre]:
			fileCategory.write(str(movie) + '\n')
		fileCategory.close()

#generowanie plików z podziałem na płeć
def partByGender(users):
	males = []
	females = []
	for man in users:
		temp = str.split(man, '|')
		if temp[2] == 'M':
			males.append(man)
		else:
			females.append(man)

	fileMale = open('user_male','w')
	for user in males:
		fileMale.write(user)
		fileMale.write('\n')
	fileMale.close()

	fileFemale = open('user_female','w')
	for user in females:
		fileFemale.write(user)
		fileFemale.write('\n')
	fileFemale.close()


#generowanie plików z podziałem na płeć, wiek i zatrudnienie
# def partByGenderAgeOccupation(users):
# 	males = []
# 	females = []
# 	print(len(users))
# 	for man in users:
# 		temp = str.split(man, '|')
# 		if temp[2] == 'M':
# 			males.append(man)
# 		else:
# 			females.append(man)

# 	fileMale = open('user_male','w')
# 	for user in males:
# 		fileMale.write(str.split(user, '|')[0])
# 		fileMale.write('\n')
# 	fileMale.close()

# 	fileFemale = open('user_female','w')
# 	for user in females:
# 		fileFemale.write(str.split(user, '|')[0])
# 		fileFemale.write('\n')
# 	fileFemale.close()

#Program główny
data = str.split(open("u.data", "r").read(), '\n')
users = str.split(open("u.user", "r").read(), '\n')

# database_divide(25)
# database_divide(50)
# database_divide(75)

# generateAverageList(500)
# partByCategory()

# partByGender(users)
