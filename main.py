from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "thisIsasecretkey23!dd"

# this is the constructor & stores all posts
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(180))
    body = db.Column(db.String(1000))
 
    def __init__(self, title, body):
        self.title = title
        self.body = body
        
    # CHECKS FOR VALID POSTS
    def empty(self):
        if self.title and self.body:
            return True
        else:
            return False


@app.route("/")
def index():
    return redirect('/blog')

# DISPLAYS ONE POST OR ALL BLOG POSTS    
@app.route('/blog')
def main_blog():
    blog_id = request.args.get('id')
    if (blog_id):
        blog = Blog.query.get(blog_id)
        return render_template("one_entry.html")
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
    #redirect ("/blog")


if __name__ == "__main__":
    app.run()
