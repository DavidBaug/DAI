from flask import request
from flask import Response
from flask import Flask, render_template
from flask import session
from pickleshare import *
import math

from pymongo import MongoClient


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


		try:
			# Existe usuario y coincide contrasenia
			if db[user]:
				if password == db[user]["passw"]:
					session['username']= user
					return render_template("index.html", user = user)
				else:
					return render_template('index.html', error = "Usuario o contraseña incorrecta")
		except Exception as e:
			return render_template('index.html', error = "Usuario o contraseña incorrectos")

	else:
		# Sesión ya iniciada
		if 'username' in session:
			username=session['username']

			return render_template('index.html', user = username)
		else:
			return render_template('index.html')

def index():
    return render_page("index.html")

@app.route('/register.html', methods = ['POST','GET'])
@app.route('/register', methods = ['POST','GET'])
def register():
	# Petición registro
	if request.method == 'POST':
		user = request.form['user']
		password = request.form['pass']

		db = PickleShareDB('DB')
		db[user] = {'passw': password}

		return render_template('index.html', user = user)
	else:
		return render_page('register.html')


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


# PRACTICA 4

# PRACTICA 4

@app.route('/mongo.html', methods = ['POST', 'GET'])
@app.route('/mongo', methods = ['POST', 'GET'])
def mongo():
	return render_page('mongo.html')

@app.route('/search_mongo', methods = ['POST', 'GET'])
def search_mongo():

	client = MongoClient("mongo", 27017)
	db = client.SampleCollections

	if request.method == 'POST':
		temporada = request.form['temporada']
		capitulo = request.form['capitulo']

		if temporada and capitulo:
			temporada = int(temporada)
			capitulo = int(capitulo)
			val = db.samples_friends.find({	"season": temporada, "number":capitulo})
		else:
			if temporada:
				temporada = int(temporada)
				val = db.samples_friends.find({	"season": temporada})
			else:
				if capitulo:
					capitulo = int(capitulo)
					val = db.samples_friends.find({	"number":capitulo})
				else:
					val = False


		return render_template("search_mongo.html", search = val)
	else:
		return render_template("search_mongo.html")

@app.route('/delete_mongo', methods = ['POST', 'GET'])
def delete_mongo():

	client = MongoClient("mongo", 27017)
	db = client.SampleCollections

	if request.method == 'POST':
		temporada = request.form['temporada']
		capitulo = request.form['capitulo']

		if temporada and capitulo and nombre:
			temporada = int(temporada)
			capitulo = int(capitulo)

			if db.samples_friends.remove({"season": temporada, "number":capitulo}):
				eliminado = True
		else:
			eliminado = False

		return render_template("delete_mongo.html", delete = eliminado)
	else:
		return render_template("delete_mongo.html")



@app.route('/modify_mongo', methods = ['POST', 'GET'])
def modify_mongo():

	client = MongoClient("mongo", 27017)
	db = client.SampleCollections

	if request.method == 'POST':
		temporada = request.form['temporada']
		capitulo = request.form['capitulo']
		nombre = request.form['nombre']

		if temporada and capitulo and nombre:
			temporada = int(temporada)
			capitulo = int(capitulo)

			if db.samples_friends.update( {	"season": temporada, "number":capitulo} , {"$set" : {"name" : nombre}}):
				modificado = True

		else:
			modificado = False

		return render_template('modify_mongo.html', modify = modificado)
	else:
		return render_template("modify_mongo.html")
