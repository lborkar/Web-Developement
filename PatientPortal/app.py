from flask import Flask,render_template,request,redirect,url_for
from flask import flash
from wtforms import Form,StringField,PasswordField,TextField,validators
from wtforms.validators import Email
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL

app=Flask(__name__)

app.config['MYSQL_HOST']='127.0.0.1'
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="Arjun@2015"
app.config["MYSQL_DB"]="patientportal"
app.config["MYSQL_CURSORCLASS"]="DictCursor"

mysql=MySQL(app)


@app.route("/")
def home():
    return render_template("home.html")

#login
@app.route("/login")
def login():
    return render_template("login.html")


class RegisterFrom(Form):
    firstname=StringField("First Name",[validators.Length(min=1,max=50)])
    lastname=StringField("Last Name",[validators.Length(min=1,max=50)])
    username=StringField("Username",[validators.Length(min=4,max=20)])
    email=StringField("Email",[validators.Length(min=6,max=50)])
    password=PasswordField("Password",
                           [
                                 validators.EqualTo("confirmpassword",message="passwords don't match"),
                                 validators.DataRequired()

                            ])
    confirmpassword=PasswordField("Confirm password")



#Register
@app.route('/register',methods=['GET','POST'])
def register():
    form=RegisterFrom(request.form)
    if request.method=='POST' and form.validate():
        # return render_template("register.html")

        firstname=form.firstname.data
        lastname= form.lastname.data
        username=form.username.data
        email=form.email.data
        password=sha256_crypt.encrypt(str(form.password.data))

        cursor=mysql.connection.cursor()
        cursor.execute("INSERT INTO users(FIRSTNAME,LASTNAME,USERNAME,EMAIL,PASSWORD) VALUES (%s,%s,%s,%s,%s)",(firstname,lastname,username,email,password))
        mysql.connection.commit()
        cursor.close()

        flash("you are successfully registered")
        redirect(url_for("login"))
    return render_template("register.html",form=form)


if __name__=='__main__':
    app.run(debug=True)



