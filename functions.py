import numpy as np
import pandas as pd 
from scipy.sparse.linalg import svds
import csv

def getRatingsData():
    ratings_data = pd.read_csv("ratings.csv")
    return ratings_data
getRatingsData()
def getBooksData():
    book_data = pd.read_csv("books1.csv")
    return book_data
def getList(df):
    output = []
    for index, row in df.iterrows():
        appendlist = []
        for i in range(len(row)):
            appendlist.append(row[i])
        output.append(appendlist)
    return output

def getUserData():
    user_data = pd.read_csv("users.csv")
    return user_data

def updateUser(userID,username,password):
    user_data = getUserData()
    usernameChanged = False
    pwdChanged = False

    if username:
        if username not in user_data.username.unique():
            user_data.set_value(userID,"username",username)
            usernameChanged = True
    if password:
        user_data.set_value(userID,"password",password)
        pwdChanged = True
    user_data.to_csv("users.csv",index=False)
    
    return usernameChanged,pwdChanged

def newUser(username,password):
    user_data = getUserData()
    if username in user_data.username.unique():
        return False
    else:
        latestId = user_data["userID"].values[-1]
        rowToWrite = [str(int(latestId)+1),str(username),str(password)]
        with open("users.csv","a") as f:
            writer = csv.writer(f)
            writer.writerow(rowToWrite)
    
        return True
        
def getUserRatings(userID):
    ratings_data = getRatingsData()
    books_data = getBooksData()    
    userRatings = ratings_data[ratings_data["userID"]==userID]
    output = pd.merge(books_data,userRatings,on="book_id").drop(columns=["genres","userID"])
    return output

def rateBook(userID,book_id,rating):
    rowToWrite = [str(userID),str(book_id),str(rating)]
    with open("ratings.csv","a") as f:
        writer = csv.writer(f)
        writer.writerow(rowToWrite)

def editRating(userID,book_id,action,rating=0):
    ratings_data = getRatingsData()
    userRatings = ratings_data[ratings_data["userID"]==userID]
    for index, row in userRatings.iterrows():
        
        if int(row["book_id"]) == int(book_id):
            
            newR = ratings_data.drop(index)
            
            newR.to_csv("ratings.csv",index=False)
            if action == "edit": 
                rateBook(userID,book_id,rating)

            


def getUserFromName(username):
    user_data = getUserData()
    if username in user_data.username.unique():
        ID = user_data[user_data["username"]==username]["userID"].tolist()
        return int(ID[0])
    else:
        return False

def checkUser(username, password):
    id = getUserFromName(username)
    user_data = getUserData()
    if id != False:
        row = user_data[user_data["username"]==username].values.tolist()
        if row[0][2] == password:
            return id
        else:
            return False
    else:
        return False







#implementing and following the tutorial given on https://beckernick.github.io/matrix-factorization-recommender/

def createMatrices():
    ratings_data = getRatingsData()
    book_data = getBooksData()

    ratings_df = pd.DataFrame(ratings_data, columns=["userID","book_id","rating"],dtype=int)
    storedUserIDs = ratings_df.userID.unique()
    user_data = getUserData()
    ratingsList = getList(ratings_data)
    for row in (user_data.index + 1):
        if not row in storedUserIDs:
            ratingsList.append([row,0,-1])
    ratings_df = pd.DataFrame(ratingsList,columns=["userID","book_id","rating"],dtype=int)
    books_df = pd.DataFrame(book_data,columns=["book_id","title","genres"])
    
    R_df = ratings_df.pivot(index="userID", columns="book_id", values="rating").replace(-1,np.nan)
    
         
    #approach 1 - fill all nan with 0 before calculating the mean
    '''
    R_df = R_df.fillna(0)
    R_matrix = np.asmatrix(R_df)
    R_mean = np.mean(R_matrix,axis=1)
    R_demeaned = R_matrix - R_mean.reshape(-1,1)
    '''

    #approach 2 - fill all nan with 0 after calculating the mean (taken from comment by Enric on the tutorial stated above)
    #this has seemed to give better ratings
    R_mean = np.array(R_df.mean(axis = 1))
    R_demeaned = R_df.sub(R_df.mean(axis=1),axis=0)
    R_demeaned = np.asmatrix(R_demeaned.fillna(0))
    U, sigma, vT = svds(R_demeaned,k=10)
    sigma = np.diag(sigma)
    predicted = np.dot(np.dot(U,sigma),vT) + R_mean.reshape(-1,1)
    predicted_df = pd.DataFrame(predicted, columns=R_df.columns).fillna(0)
    return books_df, ratings_df, predicted_df

def recommendBooks(userID):
    number = 5
    books_df,ratings_df,predicted_df = createMatrices()
    userID -= 1
    predictions_sorted = predicted_df.iloc[userID].sort_values(ascending=False)
    #merging the user ratings with the book data
    user_data = ratings_df[ratings_df.userID == (userID)]
    merged = (user_data.merge(books_df, how="left", left_on="book_id",right_on="book_id").sort_values(["rating"],ascending=False))

    recommended = (books_df[~books_df["book_id"].isin(merged["book_id"])].
        merge(pd.DataFrame(predictions_sorted).reset_index(),how="left",left_on="book_id",right_on="book_id").rename(columns ={userID:"Recommendations"}).
        sort_values("Recommendations",ascending = False).iloc[:number,:-1])

    return recommended

    




