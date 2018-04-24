from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import flask_sqlalchemy



app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = ThisisaseCretkeY


#this is the constructor 
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(255))

    def __init__(self, body, title):
        self.body = body
        self.title =title 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, username, password):
        self.username = username
        self.password = password 

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup'] # they don't ned to login to see these routes
    if request.endpoint not in allowed_routes and "username" not in session:
        return redirect("/login")

# DISPLAYS ALL THE BLOG POSTS
@app.route('/blog')
def index():
    return render_template("blog_post.html")


@app.route("/", methods=['GET', 'POST'])
def blog():
    if request.method == 'POST':
        title_name = request.form['title'] # this grabs info submitted from form to do "something" with it
        new_title = Blog(title_name) # this is a title object that will be added to DB
        db.session.add(new_title) # this passes in the object 
        db.session.commit()  # this pushes changes to DB 

    title = Blog.query.all()

    if request.method == 'POST':
        body_name = request.form['body']
        new_body = Blog(body_name)
        db.session.add(new_body)
        db.session.commit()

    body = Blog.query.all()
        

    return render_template("blog_post.html", title="Add a Blog Entry", title=title, body=body)
    return redirect ("/blog")

@app.route("/newpost")
def new_post():
        if username == username and password ==password:
            return redirect("/newpost")

@app.route("/signup")
def signup():    
    if request.method == 'POST':   # this pulls entered data 
        username = request.form['username']
        password = request.form['password']
        verify=request.form['verify']

        # TODO validate's user's data

        existing_user = User.query.filter_by(username=username).first()  # this queries db for that username. if not foudn, will create that user
        if not existing_user:
            new_user = User(username,password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username 
            return redirect('/')  # this redirects user here if user is created 

        else:
            # TODO return better response messaging 
            return "<h1>User already exists</h1>"

    return render_template("signup.html")

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
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

@app.route("/logout")
def logout():
    del session["username"]
    return redirect ("/blog")

@app.route("/index")

# redirection to welcome page 

    if not username_error and not password_error and not verify_password_error and not email_error:
        username = username
        return redirect('/welcome?username={0}'.format(username)) 
    else: 
        return render_template("index.html", username_error=username_error, password_error=password_error, 
            verify_password_error = verify_password_error,email_error=email_error,
            username=username, password=password, verify_password=verify_password, email=email)

@app.route('/welcome')
def welcome():
    username = request.args.get('username')
    return render_template("welcome.html", username=username)

if __name__ == "__main__":
    app.run()