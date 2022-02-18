from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'araujo'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

#------------------CATEGORIAS DE PRODUCTOS------

# routes
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM categoria')
    data = cur.fetchall()
    cur.close()
    return render_template('indexCategoria.html', categorias = data)

@app.route('/add_categoria', methods=['POST'])
def add_categoria():
    if request.method == 'POST':
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        activo = request.form['activo']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO categoria (codigo, nombre, descripcion,activo) VALUES (%s,%s,%s,%s)", (codigo, nombre, descripcion,activo))
        mysql.connection.commit()
        flash('Categoria Agregada con Exito')
        return redirect(url_for('Index'))

@app.route('/edit_categoria/<id>', methods = ['POST', 'GET'])
def get_categoria(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM categoria WHERE idcategoria = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('editCategoria.html',categoria = data[0])

@app.route('/update_categoria/<id>', methods=['POST'])
def update_categoria(id):
    if request.method == 'POST':
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        activo = request.form['activo']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE categoria
            SET codigo = %s,
                nombre = %s,
                descripcion = %s,
                activo = %s
            WHERE idcategoria = %s
        """, (codigo, nombre, descripcion,activo, id))
        flash('Categoria Actualizada con Exito')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete_categoria/<string:id>', methods = ['POST','GET'])
def delete_categoria(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM categoria WHERE idcategoria = {0}'.format(id))
    mysql.connection.commit()
    flash('Categoria Eliminada Exitosa')
    return redirect(url_for('Index'))

#-----------------PRODUCTOS---------------------------

@app.route('/indexProducto')
def IndexProducto():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM producto')
    data = cur.fetchall()
    cur.close()
    return render_template('indexProducto.html', productos = data)

@app.route('/add_producto', methods=['POST'])
def add_producto():
    if request.method == 'POST':
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        marca = request.form['marca']
        categoria = request.form['categoria']
        precio = request.form['precio']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO producto (codigo, nombre, descripcion,marca,categoria,precio) VALUES (%s,%s,%s,%s,%s,%s)", (codigo, nombre, descripcion,marca,categoria,precio))
        mysql.connection.commit()
        flash('Producto Guardado Exitoso')
        return redirect(url_for('IndexProducto'))

@app.route('/edit_producto/<id>', methods = ['POST', 'GET'])
def get_producto(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM producto WHERE idproducto = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('editProducto.html', producto = data[0])

@app.route('/update_producto/<id>', methods=['POST'])
def update_producto(id):
    if request.method == 'POST':
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        marca = request.form['marca']
        categoria = request.form['categoria']
        precio = request.form['precio']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE producto
            SET codigo = %s,
                nombre = %s,
                descripcion = %s,
                marca = %s,
                categoria = %s,
                precio = %s
            WHERE idproducto = %s
        """, (codigo, nombre, descripcion, marca,categoria, precio, id))
        flash('Producto Actualizado con Exito')
        mysql.connection.commit()
        return redirect(url_for('IndexProducto'))

@app.route('/delete_producto/<string:id>', methods = ['POST','GET'])
def delete_producto(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM producto WHERE idproducto = {0}'.format(id))
    mysql.connection.commit()
    flash('Producto Eliminado Exitoso')
    return redirect(url_for('IndexProducto'))

# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
