from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import db
import rev
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/', methods=['POST', 'GET'])
def index():
    session['loggedin'] = session.get('loggedin', None)
    if session.get('loggedin') is None:
        return render_template('login.html')
    return render_template('index.html')

@app.route('/reviewPage', methods=['POST', 'GET'])
def reviewPage():
    if session.get('loggedin') is None:
        return render_template('login.html')
    reviews = rev.get_all_reviews()
    return render_template('reviewPage.html', reviews=reviews)

@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if session.get('loggedin') is None:
        return render_template('login.html')
    return render_template('contact.html')

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if session.get('loggedin') is None:
        return render_template('login.html')
    users = db.get_all_users()
    result = True
    msg='User Retrieval Successful'
    return render_template('admin.html', result=result, users=users, msg=msg)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.check_user(username, password)
        print(user)
        if user is None:
            return render_template('login.html')
        else:
            session['username'] = username
            session['isadmin'] = user[4]
            session['loggedin'] = 1
            if user[4] == 1:
                users = db.get_all_users()
                result = True
                msg='User Retrieval Successful'
                return render_template('admin.html', result=result, users=users, msg=msg)
            else:
                return render_template('index.html')  
    if session.get('loggedin') is None:
        return render_template('login.html')
    return render_template('index.html')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return render_template('login.html')  

@app.route('/user_delete/<int:id>', methods=['POST', 'GET'])
def user_delete(id):
    result=db.delete_user_by_id(id)
    if result == True:
        users = db.get_all_users() 
        result = True
        msg='Delete Successful'
    else:
        msg='Delete Unsuccessful'
    return render_template('admin.html', result=result, users=users, msg=msg)  

@app.route("/user_update/<int:id>", methods=("GET", "POST"))
def save_user(id):
    if session.get("isadmin")!=1:
        session.clear()
        return render_template("login.html")
    else: 
        if request.method == "POST":
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
            admin = request.form["admin"]
            
            error = None

            if not username:
                error = "Username is required."
            elif not email:
                error = "Email is required."
            elif not password:
                error = "Password is required."

            if error is None:
                result = db.save_user(username, email, password, admin, id)
                if result==True:
                    users = db.get_all_users()   
                    result = True
                    msg = "User is saved successfully"
                    return render_template("admin.html", result=result, users=users, msg=msg)
                else:
                    error ="Failed to save a new user"                
        else:
            user = db.get_user(id)    
            return render_template("user_update.html", user=user)

@app.route("/user_create")
def user_create():
    if session.get("isadmin")!=1:
        session.clear()
        return render_template("login.html")
    else:      
        return render_template("user_create.html")

@app.route("/user_add", methods=("GET", "POST"))
def user_add():
    if session.get("isadmin")!=1:
        session.clear()
        return render_template("login.html")
    else: 
        if request.method == "POST":
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
            admin = request.form["admin"]
            
            error = None

            if not username:
                error = "Username is required."
            elif not email:
                error = "Email is required."
            elif not password:
                error = "Password is required."

            if error is None:
                result = db.add_user(username, email, password, admin)
                if result == True:
                    users = db.get_all_users()  
                    result = True
                    msg = "User is created successfully"
                    return render_template("admin.html", result=result, users=users, msg=msg)
                else:
                    error ="Failed to create a new user"
                    return render_template("user_create.html",   msg=error)
        else:
            return render_template("user_create.html")
        
@app.route('/register', methods=('GET', 'POST'))
def register():
    return render_template('register.html')
        
@app.route("/register_user", methods=("GET", "POST"))
def register_user():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        
        error = None

        if not username:
            error = "Username is required."
        elif not email:
            error = "Email is required."
        elif not password:
            error = "Password is required."

        if error is None:
            result = db.register_user(username, email, password)
            if result == True:
                users = db.get_all_users()  
                result = True
                msg = "User is created successfully"
                return render_template("login.html", result=result, users=users, msg=msg)
            else:
                error ="Failed to create a new user"
                return render_template("register_user.html",   msg=error)
    else:
        return render_template("user_create.html")

@app.route("/create_review")
def create_review():
    return render_template("create_review.html")

@app.route("/add_review", methods=("GET", "POST"))
def add_review():
    if request.method == "POST":
        username = session.get('username')
        title = request.form["title"]
        review = request.form["review"]
        
        error = None

        if not title:
            error = "Game title is required."
        elif not review:
            error = "Please give a review."

        if error is None:
            result = rev.make_review(username, title, review)
            if result == True:
                reviews = rev.get_all_reviews() 
                result = True  
                msg = "Review is created successfully"
                return render_template("reviewPage.html", result=result, reviews=reviews, msg=msg)
            else:
                error ="Failed to create a new review"
                return render_template("create_review.html",   msg=error)
    else:
        return render_template("create_review.html")
    
@app.route('/delete_review/<int:id>', methods=['POST', 'GET'])
def delete_review(id):
    result = rev.delete_review_by_id(id)
    if result == True:
        reviews = rev.get_all_reviews() 
        result = True
        msg='Delete Successful'
    else:
        msg='Delete Unsuccessful'
    return render_template('reviewPage.html', result=result, reviews=reviews, msg=msg)

@app.route("/update_review/<int:id>", methods=("GET", "POST"))
def update_review(id):
    if request.method == "POST":
        title = request.form["title"]
        review = request.form["review"]
        
        error = None

        if not title:
            error = "Game title is required."
        elif not review:
            error = "Please give a review."

        if error is None:
            result = rev.update_review(title, review, id)
            if result==True:
                reviews = rev.get_all_reviews()   
                result = True 
                msg = "Review is updated successfully"
                return render_template("reviewPage.html", result=result, reviews=reviews, msg=msg)
            else:
                error ="Failed to update review"                
    else:
        reviews = rev.get_review(id)    
        return render_template("update_review.html", reviews=reviews)

if __name__ == "__main__":
    app.run(debug=True)