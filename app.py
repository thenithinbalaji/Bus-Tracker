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
    # loading default connection string
    mongo_uri = "mongodb://localhost:27017"
    # run a python function here that initialises a local mongoDB database and its collections if they do not exist (future)

#############################################################################

# variable for checking user has logged in or not, replace this with flask session
# userbusno = 0
# update: the global variable has been replace with Flask Session and it's working


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET":
        return render_template("index.html")
    else:
        # post request i.e. login form was submitted
        college_mail_id = request.form.get("signin-email")
        password = request.form.get("signin-pswd")

        # checking if admin
        if college_mail_id == "admin@ssn" and password == "admin":
            session["admin"] = True
            return redirect(url_for("admin"))
        else:
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
                # login success

                # changing bus number of logged in user from default value of 0
                # global userbusno
                # userbusno = auth["bus_number"]

                session["userbusno"] = auth["bus_number"]
                print("Session Cookie = ", session)

                return redirect(url_for("homepage"))

        # rendering the same page (login page) if auth fails
        return render_template("index.html")


@app.route("/admin")
def admin():
    if "admin" in session:
        return render_template("adminhome.html")
    else:
        return redirect(url_for("home"))


@app.route("/adminann", methods=["POST", "GET"])
def adminann():
    if "admin" in session:
        if request.method == "GET":
            client = pymongo.MongoClient(mongo_uri)["bustracker"]["announcements"]
            str = []

            for i in client.find({}, {"_id": 0, "Message": 1}):
                str.append(i["Message"])

            return render_template("adminannounce.html", message=str)
        else:
            # posting issues
            issue = request.form.get("message")

            if len(issue) < 5:
                flash(
                    "Message too short to be posted. Please be more elaborate!",
                    category="error",
                )
            else:
                # success
                flash(
                    "Your announcement has been made successfully. All the users can see your announcement",
                    category="success",
                )

                # inserting announcements to mongoDB
                client = pymongo.MongoClient(mongo_uri)["bustracker"]["announcements"]
                data = {"Message": issue}
                client.insert_one(data)

            client = pymongo.MongoClient(mongo_uri)["bustracker"]["announcements"]
            str = []

            for i in client.find({}, {"_id": 0, "Message": 1}):
                str.append(i["Message"])

            return render_template("adminannounce.html", message=str)
    else:
        return redirect(url_for("home"))


@app.route("/adminissues")
def adminissues():
    if "admin" in session:
        client = pymongo.MongoClient(mongo_uri)["bustracker"]["issues"]
        data = []

        for i in client.find({}, {"_id": 0}):
            iss = f"Passenger from Bus {str(i['frombus'])} posted \"{i['issue']}\""
            data.append(iss)

        return render_template("adminissues.html", message=data)
    else:
        return redirect(url_for("home"))


# make this accessible from admin login alone
@app.route("/signup", methods=["POST", "GET"])
def signup():
    if "admin" in session:
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
                "bus_number": int(routeno),
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
                    "Invalid mail id, mail id must belong to ssn domain",
                    category="error",
                )
            elif len(password) < 4:
                flash("Password too short", category="error")
            elif password != re_password:
                flash("Passwords don't match", category="error")
            else:
                client.insert_one(data)
                flash("Registered Successfully", category="success")

            return render_template("create_acc.html")
    else:
        return redirect(url_for("home"))


@app.route("/homepage")
def homepage():
    # if userbusno != 0:
    if "userbusno" in session:
        # going to main page only when userbusno is present in browser session
        return render_template("homepage.html")
    else:
        # re directing to login page (function name of login page is home, not to be confused)
        return redirect(url_for("home"))


@app.route("/updates")
def updates():
    # if userbusno != 0:
    if "userbusno" in session:
        client = pymongo.MongoClient(mongo_uri)["bustracker"]["announcements"]
        str = []

        for i in client.find({}, {"_id": 0, "Message": 1}):
            str.append(i["Message"])

        return render_template("recentUpdate.html", message=str)
    else:
        # re directing to login page (function name of login page is home, not to be confused)
        return redirect(url_for("home"))


@app.route("/report", methods=["POST", "GET"])
def report():
    if request.method == "GET":
        # if userbusno != 0:
        if "userbusno" in session:
            return render_template("report.html")
        else:
            return redirect(url_for("home"))
    else:
        # posting issues
        issue = request.form.get("issue")

        if len(issue) < 5:
            flash(
                "Issue too short to be posted. Please be more elaborate!",
                category="error",
            )
        else:
            # success
            flash(
                "Your issue has been successfully submitted to admin",
                category="success",
            )

            # inserting issue to mongoDB
            client = pymongo.MongoClient(mongo_uri)["bustracker"]["issues"]
            data = {"frombus": session["userbusno"], "issue": issue}
            client.insert_one(data)

        return render_template("report.html")


@app.route("/logout")
def logout():
    # changing userbusno variable to 0 after user logs out
    # global userbusno
    # userbusno = 0
    if "userbusno" in session:
        session.pop("userbusno", None)
    if "admin" in session:
        session.pop("admin", None)

    return redirect(url_for("home"))


# route to get live locations for all buses
@app.route("/location")
def location():
    client = pymongo.MongoClient(mongo_uri)["bustracker"]["buslocation"]

    data = {}

    for document in client.find({}, {"_id": 0}):
        data[document["route"]] = [document["location"][0], document["location"][1]]

    return data


# route to get stoppings data of all buses
@app.route("/stoppings")
def stoppings():
    client = pymongo.MongoClient(mongo_uri)["bustracker"]["routes"]

    data = {}

    for document in client.find({}, {"_id": 0}):
        data[document["route"]] = document["stops"]

    return data


# route to get bus number of current logged in user
@app.route("/busno")
def busno():
    # global userbusno
    # return str(userbusno)
    if "userbusno" in session:
        return str(session["userbusno"])
    else:
        return None


# post requrest will be sent here to update the location to DB
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
