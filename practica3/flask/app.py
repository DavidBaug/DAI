from flask import request
from flask import Response
from flask import Flask, render_template
from flask import session
from pickleshare import *
import math

app = Flask(__name__)
app.secret_key='clavesita'

num_pages = 0

def render_page(page):
	if 'username' in session:
		user=session['username']
		historial =  add_page(page)
		return render_template(page, user = user, historial = historial)
	else :
		return render_template(page)

def add_page(page):
	global num_pages

	if(num_pages < 3):
		num_pages = num_pages + 1

	historial = [0]*(num_pages + 1)

	if(num_pages > 1):
		for i in range(num_pages-1, 0, -1):
			a = "historial{}".format(str(i - 1))
			b = "historial{}".format(str(i))
			session[b] = session[a]
			historial[i] = session[b]

	session["historial0"] = page
	historial[0] = page

	return historial


###############################

@app.route("/contact.html")
@app.route("/contact")
def contact():
    return render_page("contact.html")

@app.route("/collection.html")
@app.route("/collection")
def collection():
    return render_page("collection.html")

@app.route("/about.html")
@app.route("/about")
def about():
    return render_page("about.html")

@app.route("/index.html")
@app.route("/index")
@app.route("/")
def index():
	return render_page('index.html')


@app.route("/login.html", methods = ['POST','GET'])
@app.route("/login", methods = ['POST','GET'])
def login():
	# Comprobar petición de login
	if request.method == 'POST':
		user = request.form['user']
		password = request.form['pass']

		db = PickleShareDB('DB')

		# Existe usuario y coincide contrasenia
		if db[user] and password == db[user]["passw"]:
			session['username']= user
			return render_template("index.html", user = user)
		else:
			return render_template('index.html', error = "Contraseña incorrecta")

	else:
		# Sesión ya iniciada
		if 'username' in session:
			username=session['username']

			return render_template('index.html', user = username)
		else:
			return render_template('index.html')

def index():
    return render_page("index.html")

@app.route('/registrar.html', methods = ['POST','GET'])
@app.route('/registrar', methods = ['POST','GET'])
def register():
	# Petición registro
	if request.method == 'POST':
		user = request.form['user']
		password = request.form['pass']

		db = PickleShareDB('DB')
		db[user] = {'passw': password}

		return render_template('index.html', user = user)
	else:
		return render_page('registrar.html')


@app.route('/logout.html')
@app.route('/logout')
def logout():
#	historial =  add_page("logout")

	session.pop('username', None)
	global num_pages
	if(num_pages > 0):
		for i in range(0, num_pages+1):
			a = "historial{}".format(str(i))
			session.pop(a, None)

	num_pages = 0;
	return render_template("index.html")

@app.route('/settings.html', methods = ['POST','GET'])
@app.route('/settings', methods = ['POST','GET'])
def settings():
	datos = []
	historial = add_page("settings.html")
	if request.method == 'POST':
		user = request.form['user']
		password = request.form['pass']

		db = PickleShareDB('DB')
		db[user] = {'passw': password}

		datos.append(user)
		datos.append(db[user]["passw"])

		return render_template("settings.html", user = user, historial = historial, datos = datos)
	else:
		if 'username' in session:
			user = session['username']
			db = PickleShareDB('DB')
			datos.append(user)
			datos.append(db[user]["passw"])

			return render_template("settings.html", user = user, historial = historial, datos = datos)
		else:
			return redirect(redirect('index'))


@app.route('/modify', methods = ['POST','GET'])
def modify():
	datos = []
	historial = add_page("settings.html")
	if request.method == 'POST':
		user = request.form['user']
		password = request.form['pass']

		db = PickleShareDB('DB')
		db[user] = {'passw': password}

		datos.append(user)
		datos.append(db[user]["passw"])

		return render_template("index.html", user = user, historial = historial, datos = datos)
	else:
		if 'username' in session:
			user = session['username']
			db = PickleShareDB('DB')
			datos.append(user)
			datos.append(db[user]["passw"])

			return render_template("index.html", user = user, historial = historial, datos = datos)
		else:
			return redirect(redirect('index'))


@app.route('/delete', methods = ['POST','GET'])
def delete():
	datos = []
	historial = add_page("settings.html")
	if request.method == 'POST':
		user = request.form['user']
		password = request.form['pass']

		db = PickleShareDB('DB')

		print("Should be empty:",db.items())

		session.pop('username', None)
		global num_pages
		if(num_pages > 0):
			for i in range(0, num_pages+1):
				a = "historial{}".format(str(i))
				session.pop(a, None)

		num_pages = 0;
		return render_template("index.html")
	else:
		if 'username' in session:
			user = session['username']
			db = PickleShareDB('DB')

			db.uncache(db[user])

			session.pop('username', None)

			return render_template("index.html")
		else:
			return redirect(redirect('index'))
