from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "thisIsasecretkey23!dd"

# this is the constructor & stores all posts
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(180))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.owner = owner
        
    # CHECKS FOR VALID POSTS
    def empty(self):
        if self.title and self.body:
            return True
        else:
            return False

class User(db.Model):
    id  = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship("Blog", backref="owner")

    def __init__(self, username, password):
        self.username = username
        self.password = password 

    #  CHECKS FOR VALID USERNAME AND PASSWORD
    def empty(self):
        if self.username and self.password:
            return True 
        else:
            return False

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and "username" not in session:
        return redirect("/login")

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session["username"] = username
            flash("Logged In")
            return redirect('/login')
        else:
            flash("User password incorrect, or user does not exist", 'error')
    return render_template("login.html")

@app.route("/signup")
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        # TODO validate user's data

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect("/newpost")
        else:
            flash ("User already exists", 'error')
    return render_template("login.html")

@app.route("/")
def index():
    return redirect('/blog')



# DISPLAYS ONE POST OR ALL BLOG POSTS    
@app.route('/blog', methods=['POST', 'GET'])
def main_blog():
    entry_id = request.args.get('id')
    if (entry_id):
        entry = Blog.query.get(entry_id)
        return render_template("one_entry.html", title="Post", entry=entry)
    else:
        all_blogs = Blog.query.all()
        return render_template("all_blogs.html", title="Review All Posts", all_blogs=all_blogs)

# DISPLAYS THE FORM, CREATES THE NEW POST, AND RE-RENDERS FORM IF NECESSARY
@app.route("/newpost", methods=['GET', 'POST'])
def new_post():
# ALLOWS USER TO ADD A NEW BLOG POST
    if request.method == 'POST':
        title_name = request.form['title'] # this grabs info submitted from form to do "something" with it
        body_name = request.form['body']

        new_post = Blog(title_name, body_name) # this is a title object that will be added to DB

        if new_post.empty():        
            db.session.add(new_post) # this passes in the object 
            db.session.commit()  # this pushes changes to DB 
    
            url = "/blog?id=" + str(new_post.id)
            return redirect(url)
        else:
            flash("Please enter a title and share what's on your mind")
            return render_template("new_post.html", title_name=title_name, body_name=body_name)
       
    else:
        return render_template("new_post.html")

if __name__ == "__main__":
    app.run()
