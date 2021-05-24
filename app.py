from flask import Flask
from flask import render_template, request, redirect, flash
from flask.globals import session
from flaskext.mysql import MySQL
from flask_wtf.csrf import CSRFProtect
import MySQLdb.cursors
import bcrypt
import re


app=Flask(__name__)

app.secret_key='6548H62745h6e5uv65e4AQ'
csrf= CSRFProtect(app)
mysql= MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='world'
mysql.init_app(app)



@app.route("/")
def index():
    if 'username' in session:
        return redirect("/city")
    return render_template("/landing.html")


@app.route('/city')
def maincity():
    if 'username' in session:
        sql="SELECT * FROM `city`;"
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql)
        citys=cursor.fetchall()
        conn.commit()
        return render_template('citys/index.html', citys=citys)
    return redirect("/login")
@app.route('/destroy/<int:ids>')
def destroy(ids):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM `city` WHERE ID= %s",(ids))
    conn.commit()
    return redirect('/city')

@app.route('/edit/<int:ids>')
def edit(ids):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM `city` WHERE ID = %s",(ids))
    citys=cursor.fetchall()
    conn.commit()
    print(citys)
    return render_template('citys/edit.html', citys=citys)

@app.route('/update', methods=['POST', 'GET'])
def actualiza():
    _nombre=request.form['nombre']
    _code=request.form['code']
    _distro=request.form['district']
    _pob=request.form['popul']
    _id=request.form['iden']

    sql="UPDATE `city` SET `Name`='"+_nombre+"',`CountryCode`='"+_code+"',`District`='"+_distro+"',`Population`="+_pob+" WHERE ID="+_id
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    conn.commit()
    return redirect('/city')

@app.route('/create')
def create():
    if 'username' in session:
        sql="SELECT CODE FROM `country` ORDER BY `CODE` ASC"
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql)
        codes=cursor.fetchall()
        conn.commit()
        return render_template('citys/create.html',codes=codes)
    return redirect("/login")

@app.route('/store', methods=['POST'])
def storage():
    _nombre=request.form['nombre']
    _code=request.form['code']
    _distro=request.form['district']
    _pob=request.form['popul']
    sql="INSERT INTO city(`ID`, `Name`, `CountryCode`, `District`, `Population`) VALUES (NULL, '"+_nombre+"','"+_code+"', '"+_distro+"',"+_pob+");"
   
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    conn.commit()
    return redirect('/create')
    
@app.route('/login')
def logi():
    return render_template('login.html')

@app.route('/register')
def regis():
   return render_template('register.html')

@app.route('/logged', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute('SELECT * FROM accounts WHERE user = % s AND contrasena = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            msg = 'Logged in successfully !'
            return redirect('/city')
        else:
            msg = 'Incorrect username o password !'
    return render_template('login.html', msg = msg)
 
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect('/')
  
@app.route('/registred', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute('SELECT * FROM accounts WHERE user = %s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, email, password,))
            conn.commit()
            msg = 'You have successfully registered !'
            return redirect("/login")
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/countrys")
def countrys():
    if 'username' in session:
        sql="SELECT * FROM `country`;"
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql)
        countrys=cursor.fetchall()
        conn.commit()
        return render_template('countrys/country.html', countrys=countrys)
    return redirect("/login")

@app.route("/languages")
def lenguas():
    if 'username' in session:
        sql="SELECT * FROM `countrylanguage`;"
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql)
        lenguas=cursor.fetchall()
        conn.commit()
        return render_template('lenguas/lenguas.html', lenguas=lenguas)
    return redirect("/login")

if __name__=='__main__':
    app.run(debug=True)
 