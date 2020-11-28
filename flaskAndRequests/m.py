import flask
import requests as r


app = flask.Flask(__name__)

@app.route('/')
def index():
    data = r.get("https://jsonplaceholder.typicode.com/posts").json()
    return flask.render_template("index.html", posts=data)

if __name__ == '__main__':
    app.run(host="localhost", port=80, debug=True)
