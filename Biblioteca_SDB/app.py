from flask import Flask, render_template,url_for, redirect, request, flash
import pymongo
import sys
from datetime import datetime, timedelta
app = Flask(__name__)

nombre_biblioteca = 'Atenea'

cliente = pymongo.MongoClient("mongodb+srv://administrador:sectei@atenea.hfd08.gcp.mongodb.net/biblioteca_bd?retryWrites=true&w=majority")

mi_bd = cliente["biblioteca_bd"]


libros = [
    {
        "titulo" : "Claves feministas para el poderío y la autonomía de las mujeres",
        "autor" : "Marcela Legarde",
        "anio" : "1998",
        "editorial" : "Puntos de encuentro",
        "paginas_totales" : "137",
        "portada" : "",
        "pais": "España",
        "resenia": "En la primera semana de enero..."
    },
    {
        "titulo" : "Crítica del pensamiento amoroso",
        "autor" : "Mari Luz Esteban",
        "anio" : "2011",
        "editorial" : "Bellaterra",
        "paginas_totales" : "498",
        "portada" : "",
        "pais": "España",
        "resenia": "Una feminista que leía historias de amor..."
    },
    {
        "titulo" : "Neoliberalismo sexual",
        "autor" : "Ana de Miguel",
        "anio" : "2015",
        "editorial" : "Catedra",
        "paginas_totales" : "355",
        "portada" : "",
        "pais": "España",
        "resenia": "Del control de las leyes al mercado de los cuerpos"
    }
]

@app.route('/libros_many/agregar')
def agregar_libros():
    mi_col = mi_bd["libros"]
    mi_col.insert_many(libros)
    return render_template('libros_lista.html', libros = libros, nombre_biblioteca = nombre_biblioteca)

@app.route('/')
def index():
    mi_nombre = 'Elma'
    return render_template('bienvenida.html', nombre_biblioteca = nombre_biblioteca,mi_nombre = mi_nombre)

@app.route('/libros/lista')
def libros_lista():    
    return render_template('libros_lista.html', libros = libros, nombre_biblioteca = nombre_biblioteca)

@app.route('/libros/libro/<int:id>')
def libro(id):
    return render_template('libro.html', libro = libros[id], nombre_biblioteca = nombre_biblioteca)

@app.route('/libros/agregar', methods=('GET', 'POST'))
def agregar_libro():
    if request.method == 'POST':
        if not request.form['titulo']:
            flash('El titulo es requerido')
        else:
            libro_nuevo = { 
                "titulo" : request.form['titulo'],
                "autor" : request.form['autor'],
                "anio" : request.form['anio'],
                "editorial" : request.form['editorial'],
                "paginas_totales" : request.form['paginas_totales'],
                "portada" : "",
                "pais": request.form['pais'],
                "resenia": request.form['resenia']
            }
            libros.append(libro_nuevo)
            return redirect(url_for('libros_lista'))
    return render_template('agregar_libro.html', nombre_biblioteca = nombre_biblioteca)

@app.route('/usuarias/agregar', methods=('GET', 'POST'))
def agregar_usuaria():
    mi_col = mi_bd["usuarias"]
    if request.method == 'POST':
        if not request.form['nombre']:
            flash('El nombre es requerido')
        else:
            usuaria_add = { 
                "nombre" : request.form['nombre'],
                "apellidoPaterno" : request.form['apellidoPaterno'],
                "apellidoMaterno" : request.form['apellidoMaterno'],
                "correo" : request.form['correo'],
                "password" : request.form['password'],
            }
            usser = mi_col.insert_one(usuaria_add)
            print("El id de la usuaria es:", usser.inserted_id)
            return redirect(url_for('agregar_usuaria'))
    return render_template('agregar_usuaria.html', nombre_biblioteca = nombre_biblioteca)

@app.route('/usuarias/lista')
def usuarias_lista(): 
    mi_col = mi_bd["usuarias"]
    ussers =  mi_col.find() 
    return render_template('usuarias_lista.html', ussers = ussers, nombre_biblioteca = nombre_biblioteca)

@app.route('/usuarias/filtro')
def usuaria(): 
    mi_col = mi_bd["usuarias"]
    ussers =  mi_col.find({"nombre":"Karina"})
    return render_template('usuaria.html',ussers = ussers, nombre_biblioteca = nombre_biblioteca)

@app.route('/usuaria/actualiza')
def usuaria_actualiza(): 
    mi_col = mi_bd["usuarias"]
    mi_query = { "nombre": "Karina" }
    ussers =  mi_col.find(mi_query)
    nuevos_datos_usuaria = { "$set": { "correo": "karla@gmail.com", "apellidoMaterno": "Mexico" }}
    mi_col.update_one(mi_query, nuevos_datos_usuaria)
    return render_template('usuaria.html',ussers = ussers, nombre_biblioteca = nombre_biblioteca)

@app.route('/usuaria/elimina')
def usuaria_elimina(): 
    mi_col = mi_bd["usuarias"]
    mi_query = { "nombre": "Karina" }
    mi_col.delete_one(mi_query)
    ussers =  mi_col.find()
    return render_template('usuarias_lista.html', ussers = ussers, nombre_biblioteca = nombre_biblioteca)

@app.route('/prestamo/agregar',methods=('GET', 'POST'))
def agregar_prestamo():
    mi_col = mi_bd["usuarias"]
    mi_col2 = mi_bd["libros"]
    mi_col3 = mi_bd["prestamos"]
    ussers = mi_col.find()
    books = mi_col2.find()
    prestamo = mi_col3.find()

    if request.method == 'POST':
        if not request.form['fecha']:
            flash('La usuaria es requerida')
        else:
            title = request.form['titulo']
            query_libro = {"titulo": title}
            libro = mi_col2.find(query_libro)
            for element in libro:
                idLibro = element['_id']

            name = request.form['nombre']
            #apPaterno = request.form['apellidoPaterno']
            #apMaterno = request.form['apellidoMaterno']
            query_usuaria = {"nombre": name}
            usuaria = mi_col.find(query_usuaria)
            for element in usuaria:
                idUsuaria = element['_id']
                print("ID",idUsuaria)

            fechaActual = datetime.now()
            fechaEntrega = fechaActual + timedelta(days=7)
            prestamo_add = { 
                "idUsuaria" : idUsuaria,
                "idLibro" : idLibro,
                "fechaPrestamo" : fechaActual,
                "fechaEntrega" : fechaEntrega
            }
            prest = mi_col3.insert_one(prestamo_add)
    return render_template('agregar_prestamo.html',ussers = ussers, books = books, nombre_biblioteca = nombre_biblioteca)

if __name__ == "__main__":
	app.run(debug=TRUE)


