from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import flask_sqlalchemy


app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

#this is the constructor 
class Blog(db.Model):
    id = 
    date = 
    message = 

    def __initi__(self,message?):
        self.message = message


@app.route('/')
def index():
    return render_template("index.html")

#this checks length of characters and other validation  
def empty(char):
    if char:
        return True 
    else: 
        return False

def length_check(char):
    try:
        if len(char) >= 3 and len(char) <= 20:
            return True 
    except ValueError:
        return False 

def valid_email(char):
    if char.count('@') >=1:
        return True
    else:
        return False 

def multi_at_symbol(char):
    if char.count('@') <=1:
        return True
    else:
        return False 

def email_period(char):
    if char.count('.') >=1:
        return True
    else:
        return False 

def matching_passwords():
    if password == verify_password:
        return True
    else:
        return False 

@app.route("/", methods=['POST'])
def validate():
    username = request.form["username"]
    password = request.form["password"]
    verify_password = request.form['verify_password']
    email = request.form['email']

    username_error = ''
    password_error = ''
    verify_password_error = ''
    email_error = ''
    
# USERNAME VALIDATION

    if not empty(username):
        username_error = "Required Field"
        password = ''
        verify_password = ''
        password_error = "Re-enter password"
        verify_password_error = "Re-enter password"
    elif not length_check(username):
        username_error = "Field Required. Must be 3 to 20 characters"
        password = ''
        verify_password = ''
        password_error = "Re-enter password"
        invalid_password_error = "Re-enter password"
        #username = ''
    else:
        if " " in username:
            username_error = "Username cannot contain spaces"
            password =" "
            verify_password = " "
            password_error = "Re-enter password"

    
# PASSWORD VALIDATION

    if not empty(password):
        password_error = "Required Field"
        password = ''
        verify_password = ''
    elif not length_check(password):
        password_error = 'Must be 3 to 20 characters. Cannot contain spaces'
        password = ''
        verify_password = ''
        verify_password_error = "Re-enter password"
    else:
        password = password 
        password = ''

# VERIFY PASSWORD MATCHES 
 
    if not matching_passwords:
        verify_password_error = "Enter a matching password"
        password = ''
        verify_password = ''
        password_error = 'Password does not match'
    else: 
        password == verify_password
        verify_password = ''

# CHECK EMAIL

    if empty(email):
        if not valid_email(email):
            email_error = "Email must contain the @ symbol"
            password = ""
            verify_password = ""
            password_error = "Re-enter password"
            verify_password_error = "Re-enter password"
        elif not multi_at_symbol(email):
            email_error = "Email must contain only one @ symbol"
            password = ""
            verify_password = ""
            password_error = "Re-enter password"
            verify_password_error = "Re-enter password"
        elif not email_period(email):
            email_error = "Email must contact . "
            password = ""
            verify_password = ""
            password_error = "Re-enter password"
            verify_password_error = "Re-enter password"
        else:
            if " " in email:
                email_error = "Email cannot contain spaces"
                password = ""
                verify_password = ""
                password_error = "Re-enter password"
                verify_password_error = "Re-enter password"


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
