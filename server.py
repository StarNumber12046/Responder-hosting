import flask, threading
app = flask.Flask(__name__)

@app.route('/')
def main():
    return 0

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

def run():
    app.run(host='0.0.0.0', port=8080)