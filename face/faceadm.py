from flask import Flask, render_template, request, json, redirect, url_for, session, escape
from datetime import datetime
import pymysql
import uuid

app=Flask(__name__)
conn = pymysql.connect(host='localhost', user='root', password='qazw870503',
                db='face_adm', charset='utf8')
cursor = conn.cursor(pymysql.cursors.DictCursor)

@app.route('/table')
def table():
    cursor.execute("select * from member_information where Member_Grade=2")
    rows = cursor.fetchall()
    if  'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('tables.html', rows = rows, session_user_name=username_session)
    else:
        return render_template('tables.html', rows = rows)


@app.route('/mtable')
def mtable():
    return render_template('mtables.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        ID=request.form['username']
        PW=request.form['password']
        cursor.execute("select ID, Password from member_information where ID=%s",[ID])
        rows = cursor.fetchall()
        for row in rows:
            if row['Password'] == request.form['password']:
                session['username'] = request.form['username']
                return redirect(url_for('table'))  
            else:
                error = 'Invalid username or password'    
    return render_template('login.html', error = error)      
     
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

@app.route('/photo')
def photo():
    return render_template('photo.html')

@app.route("/fixmember",methods=["POST"])
def fixmember():
    #요청이 post면
    idu = uuid.uuid4()
    try:
        if request.method == 'POST':
            Member_ID = str(idu)
            ID = request.form['ID']
            Name = request.form['Name']
            Password = request.form['Password']
            Registration_Date = datetime.today().strftime('%Y.%m.%d %H:%M:%S')
            PhoneNumber = request.form['PhoneNumber']
            Member_Grade = 2
            Address = request.form['Address']
            Email = request.form['Email']
            
            cursor.execute("INSERT INTO member_information(Member_ID, ID, Name, Password, Registration_Date, PhoneNumber, Member_Grade, Address, Email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (Member_ID,ID,Name,Password,Password,Registration_Date,PhoneNumber,Member_Grade,Address,Email))
            conn.commit()
    finally:
        return redirect(url_for('table'))
    
@app.route("/fixmissing",methods=["POST"])
def fixmissing():
    #요청이 post면
    try:
        if request.method == 'POST':
            Name = request.form['Name']
            mage = request.form['missing_age']
            mheight = request.form['missing_height']
            mweight = request.form['missing_weight']
            daddress = request.form['disappearance_address']
            ddate = request.form['disappearance_date']
            MID = session['username']
            
            cursor.execute("INSERT INTO missing_person_information(Disappearance_Address, Missingperson_Name, Disappearance_Date, Missing_age, Missing_height, Missing_Weight, Member_ID) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (daddress,Name,ddate,mage,mheight,mweight,MID))
            conn.commit()
    finally:
        return redirect(url_for('table'))
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('table'))

def hello_name(user):
    return render_template('template_base.html',myname=user)
if __name__=='__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)      