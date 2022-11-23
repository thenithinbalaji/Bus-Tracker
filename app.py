from flask import Flask, render_template, send_file, request, redirect, url_for, flash
import pymongo

app = Flask(__name__)
app.config['SECRET_KEY'] = "who am i"

userbusno = 0

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET":
        return render_template("index.html")
    else:
        college_mail_id = request.form.get('signin-email')
        password = request.form.get('signin-pswd')

        client = pymongo.MongoClient("mongodb://localhost:27017")['bustracker']['logininfo']

        #auth contains the collection that matches the mail id submitted in form
        auth = client.find_one({"college_mail_id" :college_mail_id})
        
        #checking if password matches the db
        if auth != None: #making sure collection is not None
            pbool = auth['password'] == password
        
        if auth == None:
            flash('imail', category='error') #invalid mail
        elif pbool == False:
            flash('ipass', category='error') #invalid password
        else:
            global userbusno
            userbusno = auth['bus_number']
            return redirect(url_for('homepage'))

        return render_template("index.html")

@app.route("/signup",  methods=["POST", "GET"])
def signup():
    if request.method == "GET":
        return render_template("create_acc.html")
    else:
        #getting posted form data
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('pswd')
        re_password = request.form.get('confpswd')
        account_type = request.form.get('account')
        routeno = request.form.get('busroute')

        data = {
            "bus_number": routeno,  
            "name": name,  
            "college_mail_id": email,  
            "password": password,  
            "role": account_type
        }

        print(request.form)

        client = pymongo.MongoClient("mongodb://localhost:27017")['bustracker']['logininfo']

        #checking if mail id exists already
        auth = client.find_one({"college_mail_id" : email})
        if auth != None:
            flash('The email id is already registered', category='error')
        elif len(name) < 2:
            flash('Name too short', category='error')
        elif '@ssn' not in email:
            flash("Invalid mail id, mail id must belong to ssn domain", category="error")
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
    return render_template("homepage.html")

@app.route("/updates")
def updates():
    client = pymongo.MongoClient("mongodb://localhost:27017")['bustracker']['announcements']
    str = []

    for i in client.find({}, {"_id":0, "Message": 1}):
        str.append(i["Message"])

    return render_template("recentUpdate.html", message = str)

@app.route("/report")
def report():
    return render_template("report.html")

@app.route("/logout")
def logout():
    global userbusno
    userbusno = 0
    return redirect(url_for('home'))

@app.route("/location")
def location():
    client = pymongo.MongoClient("mongodb://localhost:27017")['bustracker']['buslocation']

    data = []

    for document in client.find({}, {"_id":0}):
        item = [document['route'], document['location'][0], document['location'][1]]
        data.append(item)

    return data

@app.route('/busno')
def busno():
    global userbusno
    return str(userbusno)

if __name__ == "__main__":
    app.run(debug=True)