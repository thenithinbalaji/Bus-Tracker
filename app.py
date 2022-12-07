import pymongo, os
from flask import Flask, flash, redirect, render_template, request, url_for, session

############################################################################

app = Flask(__name__)
app.config["SECRET_KEY"] = "who am i"

############################################################################

# load env variables
try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception as err:
    print(err)

# fetching mongo connection string
try:
    mongo_uri = os.environ.get("mongo_connection_string")
    print("MongoDB connection string = ", mongo_uri)
except:
    # this can be used to in code to check if connection was successful
    mongo_uri = None
    # if this is none, database error can be flashed in frontend

#############################################################################

# varible for checking user has logged in or not, replace this with flask session
userbusno = 0


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET":
        return render_template("index.html")
    else:
        college_mail_id = request.form.get("signin-email")
        password = request.form.get("signin-pswd")

        client = pymongo.MongoClient(mongo_uri)["bustracker"]["logininfo"]

        # auth contains the collection that matches the mail id submitted in form
        auth = client.find_one({"college_mail_id": college_mail_id})

        # checking if password matches the db
        if auth != None:  # making sure collection is not None
            pbool = auth["password"] == password

        if auth == None:
            flash("imail", category="error")  # invalid mail
        elif pbool == False:
            flash("ipass", category="error")  # invalid password
        else:
            # changing bus number of logged in user from default value of 0
            global userbusno
            userbusno = auth["bus_number"]
            return redirect(url_for("homepage"))

        # rendering login page if auth fails
        return render_template("index.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "GET":
        return render_template("create_acc.html")
    else:
        # getting posted form data
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("pswd")
        re_password = request.form.get("confpswd")
        account_type = request.form.get("account")
        routeno = request.form.get("busroute")

        data = {
            "bus_number": routeno,
            "name": name,
            "college_mail_id": email,
            "password": password,
            "role": account_type,
        }

        client = pymongo.MongoClient(mongo_uri)["bustracker"]["logininfo"]

        # checking if mail id exists already
        auth = client.find_one({"college_mail_id": email})
        if auth != None:
            flash("The email id is already registered", category="error")
        elif len(name) < 2:
            flash("Name too short", category="error")
        elif "@ssn" not in email:
            flash(
                "Invalid mail id, mail id must belong to ssn domain", category="error"
            )
        elif len(password) < 4:
            flash("Password too short", category="error")
        elif password != re_password:
            flash("Passwords don't match", category="error")
        else:
            client.insert_one(data)
            flash("Registered Successfully", category="success")

        return render_template("create_acc.html")


@app.route("/homepage")
def homepage():
    if userbusno != 0:
        # going to main page only if busno is not 0, meaning someone has logged in
        return render_template("homepage.html")
    else:
        # re directing to login page (function name of login page is home, not to be confused)
        return redirect(url_for("home"))


@app.route("/updates")
def updates():
    if userbusno != 0:
        client = pymongo.MongoClient(mongo_uri)["bustracker"]["announcements"]
        str = []

        for i in client.find({}, {"_id": 0, "Message": 1}):
            str.append(i["Message"])

        return render_template("recentUpdate.html", message=str)
    else:
        # re directing to login page (function name of login page is home, not to be confused)
        return redirect(url_for("home"))


@app.route("/report")
def report():
    if userbusno != 0:
        return render_template("report.html")
    else:
        return redirect(url_for("home"))


@app.route("/logout")
def logout():
    # changing userbusno variable to 0 after user logs out
    global userbusno
    userbusno = 0
    return redirect(url_for("home"))


@app.route("/location")
def location():
    client = pymongo.MongoClient(mongo_uri)["bustracker"]["buslocation"]

    data = []

    for document in client.find({}, {"_id": 0}):
        item = [document["route"], document["location"][0], document["location"][1]]
        data.append(item)

    return data


@app.route("/busno")
def busno():
    global userbusno
    return str(userbusno)


@app.route("/sharelocation", methods=["POST"])
def sharelocation():

    busno = request.json["busno"]
    lat = request.json["lat"]
    long = request.json["long"]

    client = pymongo.MongoClient(mongo_uri)["bustracker"]["buslocation"]

    client.update_one({"route": busno}, {"$set": {"location": [lat, long]}})

    return "Success"


if __name__ == "__main__":
    app.run(debug=True)
