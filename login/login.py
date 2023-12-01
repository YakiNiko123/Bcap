import hashlib
from random import randint
from flask import Flask,request,redirect,session,render_template
from flaskext.mysql import MySQL

programa = Flask(__name__)
programa.secret_key = 'nicolasvanegas'
mysql = MySQL()
programa.config['MYSQL_DATABASE_HOST']='localhost'
programa.config['MYSQL_DATABASE_PORT']=3306
programa.config['MYSQL_DATABASE_USER']='root'
programa.config['MYSQL_DATABASE_PASSWORD']=''
programa.config['MYSQL_DATABASE_DB']='punkapp_base'
mysql.init_app(programa)

conexion = mysql.connect()
cursor = conexion.cursor()



@programa.route('/')
def index():
    return render_template('login.html')


@programa.route('/login', methods = ['GET','POST'])
def login():
    if request.method =='POST':
        correo = request.form['correo_enviado']
        contrasena =request.form['contrasena']
        hashed_contrasena= hashlib.sha512(contrasena.encode("utf-8")).hexdigest()
        consulta = f"SELECT correo,contrasena FROM sesiones WHERE correo='{correo}' AND contrasena='{hashed_contrasena}'"
        
        
        cursor.execute(consulta)
        resultado = cursor.fetchall()
        conexion.commit()

        
        
        if (resultado):
            if hashed_contrasena == resultado[0][1]:
                session['logueado'] = True
                return render_template('recuperar.html')
            else:
                return render_template('login.html')
        else:
            return render_template('login.html')    
        

if __name__ == '__main__':
    programa.run(host='0.0.0.0', debug=True,port=8080)





