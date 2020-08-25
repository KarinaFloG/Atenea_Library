from flask import Flask, render_template,url_for

app = Flask(__name__)

nombre_biblioteca = 'Atenea'

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

if __name__ == "__main__":
	app.run(debug=TRUE)