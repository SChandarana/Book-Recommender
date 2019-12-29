# Web Technologies Coursework - Book recommender

#### made by jbrp94

### What's included?

#### 1)Data 

Dataset of 30 books has been created(with genres for each)
200 users have been created, each with 5 ratings (the ratings are biased based on familiar genres)
The way this has been done can be seen in "ratings.py" 
The dataset is dynamic and as more users are created and users leave more ratings, the training set of ratings and users will grow making the results of the recommender system more accurate

#### 2) Users

Users have their usernames and passwords saved along with their userID in users.csv
Users have been profiled based on their ratings, this profile will dynamically update as they leave more ratings
There is a register button to create a new user and a login button for existing users
Details on user interaction is below in the __Running information__ section 

#### 3) Algorithm

The algorithm used is the SVD Recommender Algorithm outlined in https://beckernick.github.io/matrix-factorization-recommender/
It has some tweaks however, the two main ones being how the mean values are calculated(detailed in the comments by user Enric). And also the ability to profile someone that hasn't rated any books yet. The recommender algorithm will just pick arbitrary books based on other user ratings whilst a user has no personal ratings.
You will notice that most of the recommendations tend to share similar genres as eachother showing that the system makes good recommendations given that the genre information hasn't been used when calculating the recommendations 

#### 4) Interface

The interface has been made using Flask and for the dynamic page loading, jinja2 has been used to allow me to pass variables from python to html (helps with rendering the tables etc)
This allowed for the system to be quick at responding whilst in use
GET and POST requests from forms/href links are the main way a user can traverse the website

### Running Information
- Unzip the file and navigate to the directory jbrp94_WT
- Use the command "python main.py" or "python3 main.py" (try both) to begin the server on localhost:5000
- Go to localhost:5000 in your browser
- Whilst not logged in, the user can only view the available books
- To log in, either use an existing account with the username "user__i__"(e.g. "user1") and password "password"
- This will reveal a new tab in the navbar, "User Dashboard"
- Click on this to see book recommendations on the left and the user's current rated books on the right
- Underneath there are 2 forms, one lets you rate/edit a rating on a book by selecting the book and selecting a rating. The other lets you delete a rating from the list of books you have rated
- At any point you can use the logout button and be redirected to the main page
- Note that if you ever try to access another user's information by using path traversal (i.e. changing the userID value in the address bar) the system will kick you back to the loading page