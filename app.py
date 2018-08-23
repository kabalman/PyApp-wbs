from flask import Flask, render_template, request, session, make_response, flash, url_for, redirect
import requests
from flask_restful import Api
import os
from resources.wbs import CreateWBS, DeleteWBS, ListWBS
from models.user import User
from models.wbs import WBS
import io
import csv


connectionstring = "postgresql://" + os.environ.get('PG_USER') + ":" + os.environ.get('PG_PASSWORD') + "@" + os.environ.get('PG_HOST') + "/" + os.environ.get('PG_DATABASE')



app = Flask(__name__)
app.secret_key = "uV77gcmxmSrQXwiHV7xM"

api = Api(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = connectionstring


# creates all of the tables before the first api call
@app.before_first_request
def create_tables():
    db.create_all()


# api application
api.add_resource(CreateWBS, '/api/wbs/create')
api.add_resource(DeleteWBS, '/api/wbs/delete/<string:wbs>')
api.add_resource(ListWBS, '/api/wbs/list/<string:company>/<string:businessunit>/<string:project>')


# web application
# login page
@app.route("/")
def root():
    User.logout()
    return render_template('login.html')


# home web page
@app.route("/login", methods=['POST', 'GET'])
def login_user():
    if request.method == 'GET':
        User.logout()
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['password']
        # Checks if the users login credentials are vaild if not it returns them to the login screen
        if User.login_valid(email, password):
            User.login(email)
        else:
            session['email'] = None
            error = 'Invalid credentials'
            return render_template('login.html', error=error)
        # If login details are correct the user is forwarded to their profile page
        return redirect(url_for('profile'))


@app.route("/wbs/add", methods=['POST', 'GET'])
def wbscreate():
    # This gets the company that the user was assigned to and sets that as a static value in the application so they can only create WBS Codes for their company
    user = User.get_by_email(session['email'])
    company = user.company
    if request.method == 'GET':
        return render_template('wbs.html', email=session['email'], company=company)
    else:
        # This sets variables based on what the user enters into the web form
        businessunit = request.form['businessunit']
        project = request.form['project']
        wbs = request.form['wbs']
        owner = request.form['owner']
        # This is the message data being collected to be passed as part of the api call
        message_data = {}
        message_data['company'] = company
        message_data['businessunit'] = businessunit
        message_data['project'] = project
        message_data['wbs'] = wbs
        message_data['owner'] = owner
        msg_headers = {
            'Content-Type': 'application/json'
        }
        url = 'http://127.0.0.1:5002/api/wbs/create'

        # runs the api call to create a new wbs code
        r = requests.post(url, json=message_data, headers=msg_headers, verify=False)
        if r.status_code == 201:
            flash('WBS Code added successfully')
            return render_template('wbs.html', company=company)
        elif r.status_code == 400:
            error = 'WBS Code already exists'
            return render_template('wbs.html', error=error, company=company)
        else:
            error = 'Unknown Error Occured'
            return render_template('wbs.html', error=error, company=company)


@app.route("/wbs/list")
def wbslist():
    # Gets the company the user is assigned to and shows all of the WBS codes for that company
    user = User.get_by_email(session['email'])
    company = user.company
    entries = WBS.find_by_company(company)
    return render_template('list.html', entries=entries)


@app.route("/wbs/export")
def wbsexport():
    # Exports all of the entries for the users company into a csv file that the user can download
    user = User.get_by_email(session['email'])
    company = user.company
    q = WBS.find_by_company(company)
    csv_list = [['Company', 'Business Unit', 'Project', 'WBS Code', 'Owner']]
    for each in q:
        csv_list.append(
            [
                each.company,
                each.businessunit,
                each.project,
                each.wbs,
                each.owner
            ]
        )
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerows(csv_list)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route("/profile")
def profile():
    return render_template('profile.html', email=session['email'])

# This allows you to add new users to be able to login and use the tool - this is hidden from the web page
@app.route("/user-add", methods=['POST', 'GET'])
def usercreate():
    if request.method == 'GET':
        if session['email'] is not None:
            return render_template('user.html')
        else:
            return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['password']
        company = request.form['company']
        if User.create_user(email, password, company):
            flash('User added successfully')
            return render_template('user.html')
        else:
            error = 'Failed to add user'
            return render_template('user.html', error=error)


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5002, host='0.0.0.0')
