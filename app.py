from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL



app=Flask(__name__)

mysql= MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='world'
mysql.init_app(app)

@app.route('/')
def index():
    sql="SELECT * FROM `city`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    citys=cursor.fetchall()
    print(citys)
    conn.commit()
    return render_template('citys/index.html', citys=citys)
@app.route('/destroy/<int:ids>')
def destroy(ids):
   
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM `city` WHERE ID= %s",(ids))
    conn.commit()
    
    return redirect('/')

@app.route('/edit/<int:ids>')
def edit(ids):

   return render_template('citys/edit.html')
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
 