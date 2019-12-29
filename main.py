from flask import Flask, render_template,request,redirect,Response,url_for
from functions import *
app = Flask(__name__)
logged_in = False
logged_user = False
R_error = ""
L_error = ""
@app.route("/")
def main():
    booksList = getList(getBooksData())
    if logged_in:
        return render_template("books.html",logged_in=logged_in,user=logged_user,books = booksList)
    else:
        return render_template("books.html",logged_in=logged_in,books = booksList,R_error=R_error,L_error=L_error)



@app.route("/register", methods=["POST"])
def register():
    global logged_in
    global logged_user
    global R_error
    username = request.form["username"]
    password = request.form["password"]
    if newUser(username,password):
        logged_in = True
        logged_user = getUserFromName(username)
        R_error = ""
        return redirect(url_for("main"))
    else:
        R_error = "Username already exists"
        return redirect(url_for("main"))
        

        

@app.route("/login", methods=["POST"])
def login():
    global logged_in
    global logged_user
    global L_error
    username = request.form["username"]
    password = request.form["password"]
    logged_user = checkUser(username,password)
    if logged_user:
        logged_in = True
        L_error = ""
        return redirect(url_for("main"))
    else:
        L_error = "Username/password is incorrect"
        return redirect(url_for("main"))
    

@app.route("/dashboard/<int:user>")
def dashboard(user):
    if logged_in and user == logged_user:
        booksList = getList(getBooksData())
        user_ratings_list = getList(getUserRatings(user))
        user_recommended_list = getList(recommendBooks(user))
        return render_template("dashboard.html",logged_in=logged_in,user=user,user_ratings_list=user_ratings_list, user_recommended_list=user_recommended_list, books=booksList)
    else:
        return redirect(url_for("main"))

@app.route("/addRating/<int:user>", methods=["POST"])
def addRating(user):
    if logged_in and user == logged_user:
        book = request.form["book"]
        rating = request.form["inlineRadioOptions"]
        book_id = book.split(":")
        user_ratings_list = getList(getUserRatings(user))
        action = "new"
        
        for i in range(len(user_ratings_list)):
            if int(user_ratings_list[i][0]) == int(book_id[0]):
                action = "edit"
        if action == "edit":
            editRating(user,book_id[0],"edit",rating)
        else:
            rateBook(user,book_id[0],rating)
        return redirect(url_for("dashboard",user=user))
    else:
        return redirect(url_for("main"))


@app.route("/delRating/<int:user>", methods=["POST"])
def delRating(user):
    if logged_in and user == logged_user:
        book = request.form["book"]
        book_id = book.split(":")
        editRating(user,book_id[0],"del")
        return redirect(url_for("dashboard",user=user))
    else:
        return redirect(url_for("main"))

@app.route("/logout", methods=["POST"])
def logout():
    global logged_user
    global logged_in
    logged_user = False
    logged_in = False
    return redirect(url_for("main"))


if __name__ == "__main__":
    app.run()