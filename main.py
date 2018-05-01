from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "thisIsasecretkey23!dd"

# RELATIONAL DATABASE ESTABLISHED BETWEEN BLOG & USER THROUGH FOREIGN KEY
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(180))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner
        
# CREATED USER CLASS iwth ID, username, password and posts
class User(db.Model):
    id  = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship("Blog", backref="owner")

    def __init__(self, username, password):
        self.username = username
        self.password = password 

    def __repr__(self):
        return str(self.username)

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'main_blog', 'index']
    if request.endpoint not in allowed_routes and "username" not in session:
        return redirect("/login")

@app.route("/")
def index():
    users = User.query.all()
    return render_template("index.html", users=users)

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if username == "":
            flash("Username Required")
        elif password == "":
            flash("Password Required")
        elif user and user.password == password:
            session['user'] = username    
            flash("Logged In!")
            return redirect("/newpost")
        else:
            flash('User does not exist or password does not match')
    return render_template("/login.html")

@app.route("/signup", methods =['POST', 'GET'])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        # TODO validate user's data
        if username == "":
            flash("Username required")
        if password == "":
            flash("Password Required. Must have at least 3 characters")
        elif " " in password or " "  in username:
            flash("Username or Password cannot contain any spaces")
        elif len(username) <= 2 or len(password)<=2:
            flash("Username & Password must be at least 3 characters")
        else:
            if password != verify:
                flash("Passwords must match")
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username taken. Enter another username")

        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = new_user.username
            return redirect("/newpost")
        else:
            flash ("User already exists")
            return render_template("signup.html") 
    return render_template ("signup.html") 

# DISPLAYS ONE POST OR ALL BLOG POSTS    
@app.route('/blog', methods=['POST', 'GET'])
def main_blog():
    if (request.args.get("id")):
        entry_id = request.args.get('id')
        entry = Blog.query.filter_by(id=entry_id).first()
        return render_template("one_entry.html", entry=entry)

    if (request.args.get("userid")):
        user_id =request.args.get("userid")
        entries = Blog.query.filter_by(owner_id=user_id).all()
        return render_template("all_blogs.html", entries=entries)
    entries = Blog.query.all()
    return render_template("all_blogs.html", entries=entries)
   
@app.route("/newpost")
def post():
    return render_template("new_post.html", title="New Post")

# ALLOWS USER TO ADD A NEW BLOG POST
@app.route("/newpost", methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title_name = request.form['title'] # this grabs info submitted from form to do "something" with it
        body_name = request.form['body']
        owner = User.query.filter_by(username=session['username']).first()

        title_error = ""
        body_error = ""

        if title_name == "":
            title_error = "Title Required"
        if body_name == "":
            body_error = "Content Required"

        if not title_error and not body_error:
            new_post = Blog(title_name, body_name, owner)
            db.session.add(new_post)  
            db.session.commit()  
            url = "/blog?id=" + str(new_post.id)
            return redirect(url)
        else:
            flash("Please enter a title and share what's on your mind")
            return render_template("new_post.html", title_name=title_name, body_name=body_name)

@app.route("/logout")
def logout():
    del session['username']
    return redirect('/')   

if __name__ == "__main__":
    app.run()