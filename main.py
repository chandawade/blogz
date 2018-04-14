from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "thisIsasecretkey23!dd"

#this is the constructor 
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(180))
    body = db.Column(db.String(1000))
 
    def __init__(self, body, title):
        self.body = body
        self.title =title

# DISPLAYS ALL THE BLOG POSTS
@app.route('/blog')
def index():
    return render_template("blog.html")

# CHECKS FOR EMPTY CHARACTERS 
@app.route("/newpost")
def empty(x):
    if x:
        return True
    else:
        return False

# VALIDATES CHARACTERS IN FORM INPUTS
@app.route("/newpost", methods=['GET', 'POST'])
def blog():
    title=request.form['title']
    body=request.form['body']
    title_error = ''
    body_error= ''

    if not empty(title):
        title_error = "Please add a title"
        body_error = ''
    else:
        title=title
        title = ''
    
    if not empty(body):
        body_error = "Please add content to your blog"
        title_error = ''
    else:
        body = body
        body = ''

# ALLOWS USER TO ADD A NEW BLOG POST
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
        
    return render_template("new_post.html", title=title, body=body)
    redirect ("/blog")
         



if __name__ == "__main__":
    app.run()
