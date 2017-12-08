from flask import Flask, render_template, request
from datetime import datetime

app=Flask(__name__)

@app.route('/table')
def table():
    return render_template('tables.html')

@app.route('/mtable')
def mtable():
    return render_template('mtables.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/missingregister')
def missingregister():
    return render_template('missingregister.html')

@app.route('/memberedit')
def memberedit():
    return render_template('memberedit.html')

@app.route('/missingedit')
def missingedit():
    return render_template('missingedit.html')

def hello_name(user):
    return render_template('template_base.html',myname=user)
if __name__=='__main__':
    app.run(debug=True)      