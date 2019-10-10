#./flask/app.py

from flask import Flask
from flask import request
from flask import render_template

import mandelbrot as mb

import random

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/user/<username>')
def user_greeting(username):
    return '''  <!DOCTYPE html>
                <head>
                  <link rel="stylesheet" type="text/css" href="/static/style.css">
                </head>
                <html>
                  <body>
                    <h1>Hola %s!</h1>
                    <p>Aquí tienes una foto de un gatete</p>
                    <img src='/static/images/gatete.jpg'>
                  </body>
                </html>
                ''' % (username)



@app.errorhandler(404)
def page_not_found(error):
    return "HTTP 404, not found", 404

# PARA NOTA 1- IMAGEN BINARIA

@app.route('/mandelbrot/', methods=['GET','POST'])
def datosFractal():
    return render_template('datos_mandelbrot.html')

@app.route('/pinta_mandelbrot/', methods=['GET','POST'])
def pintaFractal():
    x1 = float(request.args.get('x1'))
    x2 = float(request.args.get('x2'))
    y1 = float(request.args.get('y1'))
    y2 = float(request.args.get('y2'))

    anchura = int(request.args.get('anchura'))
    iteraciones = int(request.args.get('iteraciones'))

    mb.pintaMandelbrot(x1,y1,x2,y2,anchura, iteraciones, "fractal.png")

    return render_template('pinta_mandelbrot.html')



# PARA NOTA 2 - IMAGEN VECTORIAL

@app.route('/svg/')
def show_svg():
    rnd_list = [str(random.randint(1,100)) for x in range(17)]
    color_list = ["black","blue","yellow","gold","lawngreen","royalblue","chocolate","slategrey","plum","peru","lightpink"]

    random.shuffle(color_list)
    rectangle = '<rect x="{}%" y="{}%" width="{}%" height="{}%" stroke="{}" stroke-width="5" style="fill:{}" />'.format(*rnd_list[0:4],color_list[0],color_list[1])
    circle = '<circle cx="{}%" cy="{}%" r="{}%" stroke="{}" stroke-width="5" style="fill:{}" />'.format(rnd_list[4],rnd_list[5],str(int(rnd_list[6])/4),color_list[2],color_list[3])
    ellipse = '<ellipse cx="{}%" cy="{}%" rx="{}%" ry="{}%" stroke="{}" stroke-width="5" style="fill:{}"/>'.format(rnd_list[7],rnd_list[8],str(int(rnd_list[9])/4),str(int(rnd_list[10])/4),color_list[4],color_list[5])
    return '''
            <?xml version="1.0" encoding="UTF-8" standalone="no"?>
            <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
                {}
                {}
                {}
            </svg>
            '''.format(rectangle,circle,ellipse)
