from flask import Flask, url_for, render_template, redirect, request
import flask
from flask_pymongo import PyMongo


app = Flask(__name__, template_folder='templates')

# mongodb connection codes
app.config["MONGO_URI"] = "mongodb://localhost:27017/Games"
mongodb_client = PyMongo(app)
db = mongodb_client.db


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/games')
def games():
    return render_template('games.html')


# form section
@app.route('/register', methods=['POST', 'GET'])
def register():
    users = db.users

    if request.method == 'POST':
        existing_user = users.find_one({'email': request.form['email']})

        if existing_user is None:
            users.insert_one({'name': request.form['name'],
                              'email': request.form['email'],
                              'password': request.form['password']})
            return redirect(url_for('games'))

        return "That email already exists! Please enter a different email"

    return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    users = db.users

    if request.method == 'POST':
        login_user = users.find_one({'email': request.form['email']})

        if login_user:
            if request.form['password'] == login_user['password']:
                return redirect(url_for('games'))
        return "wrong email/ password!"

    return render_template('login.html')


@app.route('/admin-login', methods=['POST', 'GET'])
def admin_login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        if email == "jawad@gmail.com" and password == "112233":
            return redirect(url_for('admin'))

        return "wrong password/email!"

    return render_template('admin-login.html')


@app.route('/admin')
def admin():
    users = db.users.find()
    return render_template('admin.html', users=users)

@app.route('/delete', methods=['POST', 'GET'])
def delete():
    users = db.users.find()

    if request.method == 'POST':
        db.users.delete_one({"email": request.form['email_id']})

    return render_template('delete.html', users=users)


@app.route('/edit', methods=['POST', 'GET'])
def edit():

    if request.method == 'POST':
        db.users.delete_one({"email": request.form['email_id']})
        return render_template('updateUser.html')

    users = db.users.find()
    return render_template('edit.html', users=users)


@app.route('/updateUser', methods=['POST', 'GET'])
def updateUSer():
    users = db.users

    if request.method == 'POST':
        existing_user = users.find_one({'email': request.form['email']})

        if existing_user is None:
            users.insert_one({'name': request.form['name'],
                              'email': request.form['email'],
                              'password': request.form['password']})
            return redirect(url_for('edit'))

        return "That email already exists! Please enter a different email"

    return render_template('updateUser.html')



# games routes
@app.route('/snak')
def snak():
    return render_template('snak.html')

@app.route('/ColorBlast')
def ColorBlast():
    return render_template('ColorBlast.html')

@app.route('/conve')
def conve():
    return render_template('conve.html')

@app.route('/nanja')
def nanja():
    return render_template('nanja.html')

@app.route('/PlanetDefence')
def PlanetDefence():
    return render_template('PlanetDefence.html')

@app.route('/red_rect')
def red_rect():
    return render_template('red_rect.html')

if __name__ == '__main__':
    app.config['Debug'] = True
    app.run()
