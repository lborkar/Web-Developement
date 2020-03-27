from flask import  Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/more")
def more():
    return render_template("more.html")

@app.route("/thirdpage")
def thirdpage():
    return render_template("thirdpage.html")

@app.route("/hello", methods=["POST"])
def hello():
    name = request.form.get("name")
    return render_template("hello.html", name=name)



if __name__ == '__main__':
    app.run(debug=True)