from fuzzywuzzy import fuzz

dispatchers_1 = []
dispatchers_2 = []

try:
    with open("last_application_number.txt", "r") as file:
        file = file.readline()
        global_application_number = int(file)
except FileNotFoundError:
    pass


def update_global_app_num(app_num):
    with open('last_application_number.txt', 'w') as file:
        file.write(str(app_num))


def checkDispatcher(chat_id):
    for i in dispatchers_1:
        if i == chat_id:
            return 1
    for i in dispatchers_2:
        if i == chat_id:
            return 1
    return 0


def addDispatcher(chat_id):
    if not checkDispatcher(chat_id):
        if check_group(chat_id) == 1:
            dispatchers_1.append(chat_id)
        else:
            dispatchers_2.append(chat_id)


def clear():
    with open("users.txt", 'w') as file:
        file.close()


def writeUser(user_id):
    temp = 0
    with open("users.txt", 'r') as users:
        arr = users.readlines()
        for i in range(len(arr)):
            arr[i] = int(arr[i].strip('\n'))
            if arr[i] == user_id:
                temp = 1
                break
        arr = []
        users.close()
    if temp == 0:
        with open("users.txt", 'a') as users:
            users.writelines(str(user_id) + "\n")
        users.close()


def isUser(user_id):
    with open("users.txt", 'r') as users:
        arr = users.readlines()
        for i in arr:
            if int(i.strip('\n')) == user_id:
                return 1
        return 0


def check_group(num):
    with open('dispatchers_1group.txt', 'r') as dps:
        arr = dps.readlines()
        for i in range(len(arr)):
            arr[i] = arr[i].strip('\n')
            if str(num) == arr[i]:
                return 1
    with open('dispatchers_2group.txt', 'r') as dps:
        arr = dps.readlines()
        for i in range(len(arr)):
            arr[i] = arr[i].strip('\n')
            if str(num) == arr[i]:
                return 2
    return 0


def isDispatcher(num):
    tmp = 0
    with open('dispatchers_1group.txt', 'r') as dps:
        arr = dps.readlines()
        for i in range(len(arr)):
            arr[i] = arr[i].strip('\n')
            if str(num) == arr[i]:
                return 1
    if tmp == 0:
        with open('dispatchers_2group.txt', 'r') as dps:
            arr = dps.readlines()
            for i in range(len(arr)):
                arr[i] = arr[i].strip('\n')
                if str(num) == arr[i]:
                    return 1
    return 0


def similar(a, b):
    if fuzz.partial_ratio(a.lower(), b.lower()) == 100 and fuzz.ratio(a.lower(), b.lower()) == 100:
        return 100
    return fuzz.partial_ratio(a.lower(), b.lower()) - 1


def check_similarity(msg):
    with open("streets.txt", 'r', encoding="utf-8") as streets:
        arr_streets = streets.readlines()
        arr_similarity = {}
        for i in range(len(arr_streets)):
            arr_streets[i] = arr_streets[i].strip('\n')
            arr_similarity[arr_streets[i]] = similar(msg, arr_streets[i])
    arr_similarity = sorted(arr_similarity.items(), key=lambda x: x[1], reverse=True)
    streets.close()
    return arr_similarity


def check_street(msg):
    arr_similarity = check_similarity(msg)
    return arr_similarity[0][1]


def getMostSimilar(msg):
    arr_similarity = check_similarity(msg)
    return arr_similarity[0][0][0].upper() + arr_similarity[0][0][1:]


def check_house(street, msg):
    with open(f"houses/{street}.txt", 'r', encoding="utf-8") as houses:
        arr_houses = houses.readlines()
        for i in range(len(arr_houses)):
            arr_houses[i] = arr_houses[i].strip('\n')
        houses.close()
    temp = 0
    msg = msg.replace(' ', '')
    msg = msg.replace('орпус', '')
    for i in arr_houses:
        if str(msg) == str(i):
            temp = 1
            break
    if temp == 1:
        return 1
    else:
        return 0

