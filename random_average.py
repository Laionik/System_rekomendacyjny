#sprawdzanie oceny filmu
def checkID(movieID, user):
    for rate in user:
    	if int(rate[1]) == int(movieID) and int(rate[2]) >= 3:
    		return True
    return False

#obliczanie wyników
def calculateStatistic(correctSuggestion, recommendationNumber):
    return correctSuggestion / recommendationNumber * 100, 0

#sprawdzanie poprawności rekomendacji
def checkRecommendation(recommendationNumber, moviesID, user):
	correctSuggestion = 0
	for movieID in moviesID:
		if checkID(movieID, user):
			correctSuggestion += 1
	precision, auroc = calculateStatistic(correctSuggestion, recommendationNumber)
	return precision, auroc

#Losowe
def randomRecommendation(recommendationNumber, rndList, user):
    randomPrec, randomAuroc = checkRecommendation(recommendationNumber, rndList, user)
    return randomPrec

#Średnia
def averageRecommendation(recommendationNumber, avgList, user):
    avgPrec, avgAuroc = checkRecommendation(recommendationNumber, avgList, user)
    return avgPrec

#generowanie losowej listy filmów
def getRandomList(movies, recommendationNumber):
    rndList = []
    indexList = []
    for index in range(0, movies):
        indexList.append(index)

    while len(rndList) < recommendationNumber:
        id = random.randint(0, len(indexList) - 1)
        rndList.append(indexList[id])
        indexList.pop(id)
    return rndList


# Funckja główna programu
def main(recommendationNumber, randomMainList, averageMainList):
    randomPrecision = 0
    averagePrecision = 0
    randomList = randomMainList[:recommendationNumber]
    averageList = averageMainList[:recommendationNumber]

    print("Rozpoczynam sprawdzanie danych dla %d rekomendacji. Proszę czekać..." % recommendationNumber)
    time = datetime.datetime.now()
    for user in userRateList:
        randomPrecision = (randomPrecision + randomRecommendation(recommendationNumber, randomList, user)) / 2
        averagePrecision = (averagePrecision + averageRecommendation(recommendationNumber, averageList, user)) / 2  

    time = datetime.datetime.now() - time
    print("Losowy system rekomendacji: %.2f" % round(randomPrecision, 2))
    print("Średnia ocena: %.2f" % round(averagePrecision, 2))
    print("Czas sprawdzania: %.0fs" % time.seconds)


    # print("Rozpoczynam sprawdzanie danych. Trwa analiza...")


#Program główny
import random
import datetime
fileItem = open("DB\\u.item", "r")
movies = str.split(fileItem.read(), "\n")
fileItem.close()
moviesID = []
userRate = []
max_recommendation = 110
randomMainList = getRandomList(len(movies), max_recommendation)
averageMainList = str.split(open("DB\\moviesAverage", "r").read(), '\n')


userRateList = []

for i in range(0, 943):
	userRateList.append([])

for line in open("DB\\u.data", "r"):
 	templine = str.split(line, "\t")
 	userRateList[int(templine[0]) - 1].append(templine)

for i in range(10, max_recommendation+1, 20):
    main(i, randomMainList, averageMainList)