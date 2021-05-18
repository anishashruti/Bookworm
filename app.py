import os
import psycopg2
from psycopg2 import Error
import requests
from flask import Flask, session, render_template, request,redirect,jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Assigning absolute path to get image to a variable Images
Images = os.path.join('static','Images')

app = Flask(__name__)

# Include image path to application configuration
app.config['UPLOAD_FOLDER'] = Images


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine('postgresql+psycopg2://postgres:bookworm3@bw-3.cykhepzbvf9e.ap-south-1.rds.amazonaws.com:5432/bookwormdb')
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    session.clear()
    return (render_template("signin.html"))

@app.route('/signup/regi', methods=['GET','POST'])
def reg():
    # Get form information.
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        password= request.form.get("password")
        user=db.execute("INSERT INTO user_info(name,email,password) VALUES (:name, :email, :password); ",{"name": name, "email": email,"password": password})
        db.commit()
        return render_template("success.html")

@app.route('/signup', methods=['GET'])
def signup():
    return render_template("signup.html")

@app.route('/search', methods=['GET'])
def search():
    return render_template("search.html")
    

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect("/")

@app.route('/signin', methods=['GET','POST'])
def signin():
    session.clear()
    return render_template("signin.html")

@app.route('/about', methods=['GET','POST'])
def about():
    return render_template("about.html")

@app.route('/signin/verify', methods=['POST'])
def signinv():
    if request.method == "POST":
        vemail = request.form.get("email")
        name=' '
        password= request.form.get("password")
        details=db.execute("SELECT * FROM user_info where email= :email",{"email": vemail}).fetchall()
        for d in details:
            if d[1] == password:
                name=d[0]
                print(d[1])
                session["email"] = d[2]
                return render_template("search.html", name = name)
            else:
                print(d)
                return render_template("not.html")

@app.route('/search/title', methods=['GET','POST'])
def Stitle():
    return render_template("titlebase.html")

@app.route('/search/title/searching', methods=['GET','POST'])
def SearchingTitle():
    if request.method == "POST":
        title = request.form.get("title")
        query="%"+title+"%"
        allbook=db.execute("SELECT * FROM allbook where title like :query order by author",{"query": query}).fetchall()
        print(allbook)
        if len(allbook)!=0:
            return render_template("title.html",allbook=allbook)
        else:
            return render_template("nobooks.html")

@app.route('/search/title/searching/<Bisbn>')
def Book_info(Bisbn):
    allbook=db.execute("SELECT * FROM allbook where isbn=:isbn",{"isbn": Bisbn}).fetchall()
    #print(Bisbn)
    res = requests.get("https://www.googleapis.com/books/v1/volumes?q="+Bisbn)
    #print(res)
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json()
    review=db.execute("SELECT user_info.email,user_info.name, comment, rating  FROM user_info INNER JOIN review ON user_info.email= review.email WHERE bookid = :bookid",{"bookid": Bisbn}).fetchall()
    return render_template("info.html",data=data,allbook=allbook,review=review)

@app.route('/review/<Bisbn>', methods=['GET','POST'])
def review(Bisbn):
    if request.method == "POST": 
        allbook=db.execute("SELECT * FROM allbook where isbn=:isbn",{"isbn": Bisbn}).fetchall()
        res = requests.get("https://www.googleapis.com/books/v1/volumes?q="+Bisbn)
        if res.status_code != 200:
            raise Exception("ERROR: API request unsuccessful.")
        data = res.json()
        rating = request.form.get("inlineRadioOptions")
        comment = request.form.get("comment")
        currentUser = session["email"]
        user=db.execute("SELECT * FROM user_info where email= :email",{"email": currentUser}).fetchall()
        row2 = db.execute("SELECT * FROM review WHERE email = :email AND bookid = :bookid",
                    {"email": currentUser,
                     "bookid": Bisbn})
        # A review already exists
        if row2.rowcount == 1:
            return render_template("msg.html")
        else:
            rating=int(rating)      
            row = db.execute("SELECT isbn FROM allbook WHERE isbn = :isbn",{"isbn": Bisbn}).fetchone()
            bid=row[0]
            db.execute("insert into review (email,comment,bookid,rating) values(:email, :comment, :bid,:rating)",{"email": currentUser, "comment": comment, "bid": bid, "rating": rating})
            db.commit()
            review=db.execute("SELECT user_info.email,user_info.name, comment, rating  FROM user_info INNER JOIN review ON user_info.email= review.email WHERE bookid = :bookid",{"bookid": Bisbn}).fetchall()
            #print(review)
            return render_template("info.html",data=data,allbook=allbook,review=review)
    else:
        allbook=db.execute("SELECT * FROM allbook where isbn=:isbn",{"isbn": Bisbn}).fetchall()
        res = requests.get("https://www.googleapis.com/books/v1/volumes?q="+Bisbn)
        if res.status_code != 200:
            raise Exception("ERROR: API request unsuccessful.")
        data = res.json()
        return render_template('review.html',data=data,allbook=allbook)

@app.route('/search/author', methods=['GET','POST'])
def Sauthor():
    return render_template("authorbase.html")

@app.route('/search/author/searching', methods=['GET','POST'])
def SearchingAuthor():
    if request.method == "POST":
        author = request.form.get("author")
        query="%"+author+"%"
        allbook=db.execute("SELECT * FROM allbook where author like :query order by title",{"query": query}).fetchall()
        print(allbook)
        if len(allbook)!=0:
            return render_template("author.html",allbook=allbook)
        else:
            return render_template("nobooks.html")

@app.route('/search/author/searching/<Bisbn>')
def ABook_info(Bisbn):
    allbook=db.execute("SELECT * FROM allbook where isbn=:isbn",{"isbn": Bisbn}).fetchall()
    res = requests.get("https://www.googleapis.com/books/v1/volumes?q="+Bisbn)
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json()
    return render_template("info.html",data=data,allbook=allbook)


@app.route('/search/isbn', methods=['GET','POST'])
def Sisbn():
    return render_template("isbnbase.html")

@app.route('/search/isbn/searching', methods=['GET','POST'])
def SearchingIsbn():
    if request.method == "POST":
        isbn = request.form.get("isbn")
        query="%"+isbn+"%"
        allbook=db.execute("SELECT * FROM allbook where isbn like :query order by title",{"query": query}).fetchall()
        if len(allbook)!=0:
            return render_template("isbn.html",allbook=allbook)
        else:
            return render_template("nobooks.html")

@app.route('/search/isbn/searching/<Bisbn>')
def IBook_info(Bisbn):
    allbook=db.execute("SELECT * FROM allbook where isbn=:isbn",{"isbn": Bisbn}).fetchall()
    res = requests.get("https://www.googleapis.com/books/v1/volumes?q="+Bisbn)
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json()
    return render_template("info.html",data=data,allbook=allbook)

@app.route("/api/<isbn>", methods=['GET'])
def api_call(isbn):

    row = db.execute("SELECT title, author, year, isbn, \
                    COUNT(review.email) as review_count, \
                    AVG(review.rating) as average_score \
                    FROM allbook \
                    INNER JOIN review \
                    ON allbook.isbn = review.bookid \
                    WHERE isbn = :isbn \
                    GROUP BY title, author, year, isbn",
                    {"isbn": isbn})

    # Error checking
    if row.rowcount != 1:
        return jsonify({"Error": "Invalid book ISBN"}), 422

    # Fetch result from RowProxy    
    tmp = row.fetchone()

    # Convert to dict
    result = dict(tmp.items())

    result['average_score'] = float('%.2f'%(result['average_score']))

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)