# Getting Started with Bus Tracker App

This project was created using [Flask](https://flask.palletsprojects.com/en/2.2.x/) and
 <p align="center">
  <a href="#">
    <img src="https://skillicons.dev/icons?i=figma,html,css,js,flask,mongodb" />
  </a>
</p>

## Running the Server

In the project directory, you can run:

```bash
python app.py
```

Runs the app in the development mode.\
Open <http://localhost:5000> to view it in your browser. \
Read below if you face any issues while running the app.

## Test Login Creds

These creds work only if mongoDB is installed in your PC.

```text
Student User
---------------
Username: user@ssn
Password: user
```

```text
Bus Tracker Admin
--------------
Username: admin@ssn
Password: admin
```

## Missing Modules

Since the app uses a specific version of certain modules, it is highly recommended to create a virtual environment and then install the modules from requirements.txt

```bash
python -m virtualenv venv
venv/scripts/activate
```

Install modules from requirements.txt using:

```bash
pip install -r requirements.txt
```

## MongoDB Errors

You need MongoDB installed in your PC to fix this error. The app takes care of initialising a database with dummy values, once mongodb is installed.

## Map API

You might see "**For developement purposes only**" or "**Map didn't load correctly**" errors in homepage. You need to generate google maps API key and update it in homepage.html script tag to fix this error.
\
**NOTE:** The app will work perfectly even without the key. The key is to remove the map overlay text.
\
[https://developers.google.com/maps/documentation/embed/get-api-key](https://developers.google.com/maps/documentation/embed/get-api-key)
