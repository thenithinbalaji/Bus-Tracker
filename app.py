import pymongo, os
from flask import Flask, flash, redirect, render_template, request, url_for, session

############################################################################

app = Flask(__name__)
app.config["SECRET_KEY"] = "who am i"
database_name = "bustrackerapp"  # make sure another db in same name doesn't exist, change this name to your custom one
############################################################################

# load env variables, "mongo uri" is in env
try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception as err:
    print(err)

# fetching mongo connection string
try:
    mongo_uri = os.environ.get("mongo_connection_string")
    print("MongoDB connection string fetched from env = ", mongo_uri)
except:
    # loading default connection string
    mongo_uri = "mongodb://localhost:27017"
    print("MongoDB connection string default, localhost db = ", mongo_uri)

# initialises a mongoDB database and its collections if they do not exist
myclient = pymongo.MongoClient(mongo_uri)
dblist = myclient.list_database_names()

if database_name in dblist:
    print(f"The '{database_name}' database exists")
else:
    mydb = myclient[database_name]

    logincol = mydb["logininfo"]
    logindata = {
        "bus_number": 1,
        "student_id": 1234567,
        "name": "Nithin",
        "college_mail_id": "user@ssn",
        "password": "user",
        "role": "Passenger",
    }
    logincol.insert_one(logindata)

    routecol = mydb["routes"]
    routesdata = [
        {
            "route": 1,
            "stops": [[13.0067, 80.2206], [12.9516, 80.1462], [12.901, 80.2279]],
        },
        {
            "route": 2,
            "stops": [[12.9815, 80.218], [12.8459, 80.2265], [12.7897, 80.2216]],
        },
        {
            "route": 3,
            "stops": [
                [12.9249, 80.1],
                [12.8866, 80.0216],
                [12.8439, 80.0597],
                [12.9516, 80.1462],
            ],
        },
        {
            "route": 4,
            "stops": [
                [13.0009, 80.1194],
                [12.9524, 80.0409],
                [12.823, 80.0447],
                [12.8866, 80.0216],
            ],
        },
    ]
    routecol.insert_many(routesdata)

    issuecol = mydb["issues"]
    issuedata = {"frombus": 2, "issue": "hi i am facing breakdown at kk nagar"}
    issuecol.insert_one(issuedata)

    annoucementscol = mydb["announcements"]
    anndata = {"Message": "Bus 4 will leave in 5 mins"}
    annoucementscol.insert_one(anndata)

    locationcol = mydb["buslocation"]
    locdata = [
        {
            "route": 1,
            "location": [12.9171, 80.1923],
        },
        {
            "route": 3,
            "location": [12.915, 80.072],
        },
        {
            "route": 4,
            "location": [12.9788, 80.0605],
        },
        {
            "route": 2,
            "location": [12.901, 80.2279],
        },
    ]
    locationcol.insert_many(locdata)

    print(f"Database named {database_name} has been created in localhost")


#############################################################################


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
            client = pymongo.MongoClient(mongo_uri)[database_name]["logininfo"]

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
            client = pymongo.MongoClient(mongo_uri)[database_name]["announcements"]
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
                client = pymongo.MongoClient(mongo_uri)[database_name]["announcements"]
                data = {"Message": issue}
                client.insert_one(data)

            client = pymongo.MongoClient(mongo_uri)[database_name]["announcements"]
            str = []

            for i in client.find({}, {"_id": 0, "Message": 1}):
                str.append(i["Message"])

            return render_template("adminannounce.html", message=str)
    else:
        return redirect(url_for("home"))


@app.route("/adminissues")
def adminissues():
    if "admin" in session:
        client = pymongo.MongoClient(mongo_uri)[database_name]["issues"]
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

            client = pymongo.MongoClient(mongo_uri)[database_name]["logininfo"]

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
        client = pymongo.MongoClient(mongo_uri)[database_name]["announcements"]
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
            client = pymongo.MongoClient(mongo_uri)[database_name]["issues"]
            data = {"frombus": session["userbusno"], "issue": issue}
            client.insert_one(data)

        return render_template("report.html")


@app.route("/logout")
def logout():
    if "userbusno" in session:
        session.pop("userbusno", None)
    if "admin" in session:
        session.pop("admin", None)

    return redirect(url_for("home"))


# route to get live locations for all buses
@app.route("/location")
def location():
    client = pymongo.MongoClient(mongo_uri)[database_name]["buslocation"]

    data = {}

    for document in client.find({}, {"_id": 0}):
        data[document["route"]] = [document["location"][0], document["location"][1]]

    return data


# route to get stoppings data of all buses
@app.route("/stoppings")
def stoppings():
    client = pymongo.MongoClient(mongo_uri)[database_name]["routes"]

    data = {}

    for document in client.find({}, {"_id": 0}):
        data[document["route"]] = document["stops"]

    return data


# route to get bus number of current logged in user
@app.route("/busno")
def busno():
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

    client = pymongo.MongoClient(mongo_uri)[database_name]["buslocation"]

    client.update_one({"route": busno}, {"$set": {"location": [lat, long]}})

    return "Success"


if __name__ == "__main__":
    app.run()
