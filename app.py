from flask import Flask,render_template, request,redirect, url_for
import os
import dbase as db

template_dir = os.path.dirname(os.path.abspath((__file__)))
template_dir = os.path.join(template_dir,'templates')

app=Flask(__name__, template_folder = template_dir)


@app.route('/')
def inicio():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM usuario")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('/index.html', data=insertObject)

@app.route('/usuario', methods=['POST'])
def adicionar():
    username = request.form['username']
    email = request.form['email']
    name = request.form['name']
    password = request.form['password']

    if username and email and name and password:
        cursor = db.database.cursor()
        sql = "INSERT INTO usuario (username, email, name, password) VALUES (%s, %s, %s, %s)"
        data = (username, email, name, password)
        cursor.execute(sql, data)
        db.database.commit()
        return redirect(url_for('inicio'))
    else:
        return notFound()
    
    
@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM usuario WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('inicio'))

@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    username = request.form['username']
    email = request.form['email']
    name = request.form['name']
    password = request.form['password']

    if username and email and name and password:
        cursor = db.database.cursor()
        sql = "UPDATE usuario SET username = %s, email= %s,name = %s, password = %s WHERE id = %s"
        data = (username,email, name, password, id)
        cursor.execute(sql, data)
        db.database.commit()
        return redirect(url_for('inicio'))
    else:
        return notFound()

@app.errorhandler(404)
def notFound(error=None):
    message ={
        'message': 'No encontrado ' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response



if __name__ == '__main__':
    app.run(port=5000, debug=True)
