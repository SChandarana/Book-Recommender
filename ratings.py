import csv
import random

#Code to create a user ratings database. Works by picking a set of favourite genres for a user and 
#then rating books with a bias for books that have matching genres

number_of_users = 200
with open("books1.csv","r") as books:
    data = csv.reader(books)
    
    genres = [0 for i in range(30)]
    for row in data:
        if row[0] == "book_id":
            continue
        genres[int(row[0])] = row[2].split(":")

with open('ratings.csv',"w",newline="") as ratings:
    writer = csv.writer(ratings)
    writer.writerow(["userID","book_id","rating"])
    user_Ratings = {}

    for userID in range(1,number_of_users+1):
        if not userID in user_Ratings:
            user_Ratings[userID] = []

        fave_genres = genres[random.randint(0,29)]
        for i in range(5):
            book = random.randint(0,29)
            while book in user_Ratings[userID]:
                book = random.randint(0,29)
            user_Ratings[userID].append(book)
            minRating = 0
            for genre in genres[book]:
                if genre in fave_genres:
                    minRating += 1
            rating = random.randint(minRating,5)
            rowToWrite = [str(userID),str(book),str(rating)]
            writer.writerow(rowToWrite) 

with open("users.csv","w",newline="") as users:
    writer = csv.writer(users)
    writer.writerow(["userID","username","password"])
    for i in range(1,number_of_users+1):
        username = "user" + str(i)
        rowToWrite = [str(i),username,"password"]
        writer.writerow(rowToWrite)

            

