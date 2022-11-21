from flask import Flask, render_template, send_file, request, redirect, url_for

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET":
        return render_template("index.html")
    else:
        print(request.form)
        return redirect(url_for('homepage'))

@app.route("/signup")
def signup():
    return render_template("create_acc.html")

@app.route("/homepage")
def homepage():
    return render_template("homepage.html")

@app.route("/updates")
def updates():
    return render_template("recentUpdate.html")

@app.route("/report")
def report():
    return render_template("report.html")

if __name__ == "__main__":
    app.run(debug=True)