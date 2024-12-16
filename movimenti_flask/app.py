from flask import Flask, render_template, request
import AlphaBot

app = Flask(__name__)
MY_ADDRESS = ("0.0.0.0", 9090)
BUFFER_SIZE = 4096
alice = AlphaBot.AlphaBot()

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #print(request.form.get('movimento'))
        if request.form.get('movimento') == '▲':
            print("avanti")
            alice.forward()
        elif  request.form.get('movimento') == '◄':
            print("sinistra")
            alice.left()
        elif  request.form.get('movimento') == '►':
            print("destra")
            alice.right()
        elif  request.form.get('movimento') == '▼':
            print("indietro")
            alice.backward()
        elif  request.form.get('movimento') == '■':
            print("stop")
            alice.stop()
        else:
            print("Unknown")
    elif request.method == 'GET':
        return render_template('index.html')
    
    return render_template("index.html")

if __name__ == '__main__':
    alice.stop()
    
    app.run(debug=True, host='0.0.0.0')