#sprawdzanie oceny filmu
def Check_Id(movieID, user):
    for rate in user:
        print(int(rate[1]))
        print(int(rate[2]))
        print()
        if int(rate[1]) == int(movieID) and int(rate[2]) >= 3:
            return True
    return False

#obliczanie wyników
def Calculate_statistic(correctSuggestion, recommendationNumber):
    return correctSuggestion / recommendationNumber * 100, 0

#sprawdzanie poprawności rekomendacji
def Check_recommendation(recommendationNumber, movies_id, user):
    correctSuggestion = 0
    for movieID in movies_id:
        if Check_Id(movieID, user):
            correctSuggestion += 1
    precision, auroc = Calculate_statistic(correctSuggestion, recommendationNumber)
    return precision, auroc

def Calculate_recommendation(recommendationNumber, rate_list, user):
    prec, auroc = Check_recommendation(recommendationNumber, rate_list, user)
    return prec


#generowanie losowej listy filmów
def Get_random_list(movies, recommendationNumber):
    rndList = []
    indexList = []
    for index in range(0, movies):
        indexList.append(index)

    while len(rndList) < recommendationNumber:
        id = random.randint(0, len(indexList) - 1)
        rndList.append(indexList[id])
        indexList.pop(id)
    return rndList


def Create_complex_list(number): 
    user_learn_list = []
    user_test_list = []
    user_category_list = []

    for i in range(0, 943):
        user_learn_list.append([])
        user_test_list.append([])

    for line in open("DB\\" + str(number) + '_test', "r"):
        templine = str.split(line, "\t")
        user_test_list[int(templine[0]) - 1].append(templine)

    for line in open("DB\\" + str(number) + '_learn', "r"):
        templine = str.split(line, "\t")
        user_learn_list[int(templine[0]) - 1].append(templine)

    for i in range(0, 943):
        user_category_list.append([])
        for x in range(0, 19):
            user_category_list[i].append(0)

    return user_learn_list, user_test_list, user_category_list
    # print("Rozpoczynam sprawdzanie danych za pomocą algorytmu złożonego. Trwa analiza...")
 
def Get_movies_rank_list():
    movies_rank_list = []
    file_index = 0
    for i in range(0, 19):
        movies_rank_list.append([])
        for line in open("DB\\movies" + str(file_index), 'r'):
            temp = str.split(line.replace('\n', ''), ' ')
            if len(temp) == 2:
                temp[1] = float(temp[1])
                movies_rank_list[i].append(temp)
        movies_rank_list[i].sort(key=lambda x: x[1], reverse=True)
        file_index += 1
    
    return movies_rank_list


def Get_categories(movies):
    genres = []
    for i in range(0, len(movies)):
        genres.append([])
        for x in range(0, 19):
            temp = str.split(movies[i], '|')
            genres[i].append(int(temp[5+x]))
    return genres

def User_add_categories(user_id, movie_id, rate_number):
    if rate_number > 3:
        temp = movies_category[movie_id]
        for x in range(0, 19):
            user_category_list[user_id][x] += temp[x]

# Funckja główna programu
def Main_simple_algorithm(recommendationNumber, random_main_list, average_main_list):
    randomPrecision = 0
    averagePrecision = 0
    randomList = random_main_list[:recommendationNumber]
    averageList = average_main_list[:recommendationNumber]

    print("Rozpoczynam sprawdzanie danych dla %d rekomendacji. Proszę czekać..." % recommendationNumber)
    time = datetime.datetime.now()
    for user in user_all_rate_list:
        randomPrecision = (randomPrecision + Calculate_recommendation(recommendationNumber, randomList, user)) / 2
        averagePrecision = (averagePrecision + Calculate_recommendation(recommendationNumber, averageList, user)) / 2  

    time = datetime.datetime.now() - time
    print("Losowy system rekomendacji: %.2f" % round(randomPrecision, 2))
    print("Średnia ocena: %.2f" % round(averagePrecision, 2))
    print("Czas sprawdzania: %.0fs" % time.seconds)


def Main_category(user_learn_list, user_test_list):
    print("Rozpoczynam sprawdzanie danych na podstawie ulubionej kategorii filmu. Trwa analiza...")
    time = datetime.datetime.now()
    best_category = []
    recommendation_category = []
    recommendation_number = 10
    category_precision = 0
    for item in user_learn_list:
        for rate in item:
            User_add_categories(int(rate[0]) - 1, int(rate[1]), int(rate[2]))

    for item in user_category_list:
        best_category.append(item.index(max(item)))

    for item in best_category:
        recommendation_category.append(list(x[0] for x in movies_rank_list[item][:recommendation_number]))

    for user in user_test_list:
        # tu coś do ogarnięcia bo chyba nie tak jest lista przekazywana
        category_precision = (category_precision + Calculate_recommendation(recommendation_number, recommendation_category[int(user[0][0]) - 1], user)) / 2
        break

    time = datetime.datetime.now() - time
    print("Ulubiona kategoria: %.2f" % round(category_precision, 2))
    print("Czas sprawdzania: %.0fs" % time.seconds)
    

#Program główny
import random
import datetime
file_item = open("DB\\u.item", "r")
movies = str.split(file_item.read(), "\n")
file_item.close()
movies_id = []
user_rate = []
max_recommendation = 110
random_main_list = Get_random_list(len(movies), max_recommendation)
average_main_list = str.split(open("DB\\moviesAverage", "r").read(), '\n')
movies_rank_list = Get_movies_rank_list()
movies_category = Get_categories(movies)

user_all_rate_list = []

for i in range(0, 943):
    user_all_rate_list.append([])

for line in open("DB\\u.data", "r"):
 	templine = str.split(line, "\t")
 	user_all_rate_list[int(templine[0]) - 1].append(templine)

# for i in range(10, max_recommendation+1, 20):
#     Main_simple_algorithm(i, random_main_list, average_main_list)

user_learn_list, user_test_list, user_category_list = Create_complex_list(25)
Main_category(user_learn_list, user_test_list)

# user_learn_list, user_test_list, user_category_list = Create_complex_list(50)


# user_learn_list, user_test_list, user_category_list = Create_complex_list(75)
