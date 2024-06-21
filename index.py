from flask import Flask

from flask import render_template,redirect,request,Response,session

from flask_mysqldb import MySQL,MySQLdb

from flask_sqlalchemy import SQLAlchemy



app=Flask(__name__,template_folder='templates')


app.config['MYSQL_HOST']='localhost'

app.config['MYSQL_USER']='root'

app.config['MYSQL_PASSWORD']='19961004Omar.'

app.config['MYSQL_DB']='tienda'

app.config['MYSQL_CURSORCLASS']='DictCursor'

mysql=MySQL(app)



@app.route('//pagina principal')

def pagina_principal():

    return render_template('index.html')

@app.route('//iniciar sesion')

def inicio_de_sesion():

    return render_template('iniciar_sesion.html')

@app.route('//registrar usuario')

def registro_usuario():

    return render_template('registro.html')

@app.route('//busqueda')

def search():

    return render_template('busqueda.html')


@app.route('//carrito')

def cart():

    return render_template('carrito.html')

@app.route('//tienda')

def tienda():

    return render_template('tienda.html')

@app.route('//nosotros')

def nosotros():

    return render_template('nosotros.html')

@app.route('//contacto')

def contacto():

    return render_template('contacto.html')





if __name__ == '__main__':

    app.secret_key="omar"

    app.run(debug=True,port=5017)