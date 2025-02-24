from flask import Flask, render_template, redirect, url_for, make_response, request
import sqlite3
import jwt
#import AlphaBot

app = Flask(__name__)
MY_ADDRESS = ("0.0.0.0", 9090)
BUFFER_SIZE = 4096
#alice = AlphaBot.AlphaBot()

def validate(username, password):
    completion = False
    con = sqlite3.connect('./python/alphabot/flask_accesso_movimento/MasoeroPollicino.db')
    #with sqlite3.connect('static/db.db') as con:
    cur = con.cursor()
    cur.execute("SELECT password FROM UTENTI WHERE username = ?", (username,))
    stored_password = cur.fetchone()
    if stored_password and check_password(stored_password[0], password):
        return True
    else:
        return False

def check_password(hashed_password, user_password):
    return hashed_password == user_password

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['e-mail']
        print(username)
        password = request.form['password']
        print(password)
        completion = validate(username, password)
        if completion ==False:
            error = 'Invalid Credentials. Please try again.'
        else:
            response = make_response(redirect(url_for('index')))
            response.set_cookie("username", username, max_age = 60*60*24)
            
            return response
    return render_template('login.html', alert=error)

@app.route("/create_account", methods=['GET','POST'])
def create_account():
    if request.method == 'POST':
        con = sqlite3.connect('./python/alphabot/flask_accesso_movimento/MasoeroPollicino.db')
        cur = con.cursor()
        username = request.form['e-mail']
        print(username)
        password = request.form['password']
        print(password)
        cur.execute('''INSERT INTO UTENTI VALUES (?,?)''', (username, password))
        con.commit()
        return redirect(url_for('login'))
    return render_template('create_account.html')

@app.route("/index", methods=['GET', 'POST'])
def index():
    username = request.cookies.get("username")  # Recupera il cookie "username"
    if not username:
        return redirect(url_for('login'))  # Reindirizza alla pagina di login se non autenticato
    if request.method == 'POST':
        #print(request.form.get('movimento'))
        if request.form.get('movimento') == '▲':
            print("avanti")
            #alice.forward()
        elif  request.form.get('movimento') == '◄':
            print("sinistra")
            #alice.left()
        elif  request.form.get('movimento') == '►':
            print("destra")
            #alice.right()
        elif  request.form.get('movimento') == '▼':
            print("indietro")
            #alice.backward()
        elif  request.form.get('movimento') == '■':
            print("stop")
            #alice.stop()
        elif  request.form.get('movimento') == '⌂':
            print("uscita con cookie")
            #alice.stop()
            return redirect(url_for('login'))
        elif  request.form.get('movimento') == 'Ð':
            print("uscita")
            #response = make_response(redirect(url_for('login')))
            #response.delete_cookie("username")  # Rimuove il cookie "username"
            #return response
            #alice.stop()
            return redirect(url_for('logout'))
        else:
            print("Unknown")
        return render_template('index.html')
    elif request.method == 'GET':
        return render_template('index.html')

@app.route("/logout")
def logout():
    response = make_response(redirect(url_for('login')))
    response.delete_cookie("username")  # Rimuove il cookie "username"
    return response

@app.route('/')
def home():
    username = request.cookies.get("username")  # Recupera il cookie "username"
    if not username:
        return redirect(url_for('login'))  # Reindirizza alla pagina di login se non autenticato
    return redirect(url_for('index'))

if __name__== "__main__":
    #alice.stop()
    
    app.run(debug=True, host='0.0.0.0')
    