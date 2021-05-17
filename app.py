from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL



app=Flask(__name__)

@app.route("/")
def index():

    return render_template('/landing-page.html')

mysql= MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='world'
mysql.init_app(app)

@app.route('/city')
def maincity():
    sql="SELECT * FROM `city`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    citys=cursor.fetchall()
    conn.commit()
    return render_template('citys/index.html', citys=citys)

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

@app.route('/update', methods=['POST'])
def method_name():
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
   return render_template('citys/create.html')


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

    return render_template('citys/create.html')



if __name__=='__main__':
    app.run(debug=True)
 