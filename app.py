import os
import datetime
import calendar

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import DEFAULT_PBKDF2_ITERATIONS, check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from helpers import apology, login_required, php, distance, allowed_file



# Configure application
app = Flask(__name__)
app.config['SECRET_KEY'] = "thisissecret"
UPLOAD_FOLDER = '/static/faces'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Date and time
time = datetime.datetime.now()

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["php"] = php

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set perimeter radius constant
radius = 40
now = datetime.datetime.now()
access_type = ''
user_name = ''
image_path = ''

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://raymundjacquez:test1234@localhost/timeinapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

db = SQLAlchemy(app)

class Users(db.Model):
    """ User table """
    id = db.Column(db.Integer, 
            primary_key=True)
    name = db.Column(db.String(80), 
            nullable=False)
    lastname = db.Column(db.String(80), 
            nullable=False)
    pw_hash = db.Column(db.String(500), 
            unique=True, 
            nullable=False)
    email = db.Column(db.String(120), 
            unique=True, 
            nullable=False)
    store_id = db.Column(db.Integer, 
            db.ForeignKey('stores.id'),
            nullable=False)
    face = db.Column(db.String(120), 
            unique=True)
    role = db.Column(db.String(20),  
            nullable=False)

class Stores(db.Model):
    """ List of all stores  with respective coordinates """
    id = db.Column(db.Integer, 
            primary_key=True)
    name = db.Column(db.String(80), 
            unique=True, 
            nullable=False)
    longitude = db.Column(db.String(80), 
            unique=True, 
            nullable=False)
    latitude = db.Column(db.String(80), 
            unique=True, 
            nullable=False)

class Timesheet(db.Model):
    """ Records clockin time"""
    id = db.Column(db.Integer, 
            primary_key=True)
    user_id = db.Column(db.Integer, 
            db.ForeignKey('users.id'), 
            nullable=False)
    week = db.Column(db.String(2), 
            nullable=False)
    day = db.Column(db.String(2), 
            nullable=False)
    month = db.Column(db.String(2), 
            nullable=False)
    year = db.Column(db.String(4), 
            nullable=False)
    time_in = db.Column(db.String(20), 
            nullable=False)
    time_out = db.Column(db.String(20), 
            nullable=False)


class Timeoff(db.Model):
    """ Records of requests """
    id = db.Column(db.Integer, 
            primary_key=True)
    user_id = db.Column(db.Integer, 
            db.ForeignKey('users.id'),
            nullable=False)
    timestamp = db.Column(db.String(40), 
            nullable=False)
    from_off = db.Column(db.String(20), 
            nullable=False)
    to_off = db.Column(db.String(20), 
            nullable=False)
    reason = db.Column(db.String(120), 
            nullable=False)
    status = db.Column(db.String(20), 
            nullable=False)


    def __repr__(self):
        return '<user %r>' % self.username

@app.context_processor
def inject_user():
    access = access_type
    user = user_name
    image = image_path
    return dict(access=access, user=user, image=image)



@app.route("/add_store", methods=["POST"])
@login_required
def add_store():

    input = request.form.get("coordinates")
    name = request.form.get("store_name")

    if not name and not input:
        flash("One or more fields are empty")
        return redirect("/admin")

    coordinates = input.split(", ")

    if len(coordinates) < 2:
        flash("Invalid coordinates")
        return redirect("/admin")

    longitude = coordinates[0]
    latitude = coordinates[1]

    new_store = Stores(name=name, longitude=longitude, latitude=latitude)
    
    try:
        db.session.add(new_store)
        db.session.commit()
    except:
        flash("ERROR: Store name or Coordinates may already exist in Database.")
        return redirect("/admin")

    flash("Store added")

    return redirect("/admin")


@app.route("/pin_required")
@login_required
def pin_required():
    
    user_pin = request.form.get("pin")
    user = Pin.query.filter_by(user_id=request.form.get("user_id")).first()

    if user.pin != user_pin:
        flash("Invalid Pin")
        return redirect("/people")


@app.route("/admin")
@login_required
def admin_page():
    # Get all time off requests of user
    time_off = Timeoff.query.order_by(Timeoff.id.desc()).all()

    # Create a list of all requests
    t_off = []

    for data in time_off:
        t_off.append(data)
    return render_template("admin.html", all_request=t_off)

@app.route("/profile", methods=["GET", "POST"])
@login_required
def prfile():
    return render_template("profile.html")

@app.route("/action_toff", methods=["POST"])
@login_required
def request_action():

    if request.form.get("action") == 'approved':
        record = Timeoff.query.filter_by(id=request.form.get("recId")).first()

        record.status = 'Approved'
        db.session.commit()

        flash('Request Approved!')

    if request.form.get("action") == 'declined':
        record = Timeoff.query.filter_by(id=request.form.get("recId")).first()

        record.status = 'Declined'
        db.session.commit()

        flash('Request Declined!')

    return redirect("/admin")

@app.route("/edit_toff", methods=["POST"])
@login_required
def edit_request():

    if not request.form.get("id"):
        flash("record not found")
        return redirect("/timeoff")

    start = request.form.get("start").split("-")
    end = request.form.get("end").split("-")

    if not request.form.get("end"):
        end_date = start[2] + "/" + start[1] + "/" + start[0]
    else:
        end_date = end[2] + "/" + end[1] + "/" + end[0]

    mod = Timeoff.query.filter_by(id=request.form.get("id")).first()

    mod.from_off = start[2] + "/" + start[1] + "/" + start[0]
    mod.to_off = end_date
    mod.reason = request.form.get("reason")
    mod.timestamp = str(datetime.datetime.now().strftime("%A, %d %B %Y at %H:%M")) + "  (Modified)"

    db.session.commit()

    flash("Changes saved")

    return redirect("/timeoff")

@app.route("/delete_toff", methods=["POST"])
@login_required
def delete_request():

    if not request.form.get("recId"):
        flash("record not found")
        return redirect("/timeoff")
    
    record = Timeoff.query.filter_by(id=request.form.get("recId")).first()

    db.session.delete(record)
    db.session.commit()

    flash("Successfuly deleted")

    if request.form.get("page") == 'admin':
        return redirect("/admin")

    return redirect("/timeoff")

@app.route("/report", methods=["POST"])
@login_required
def report():
    """ Save clock in correction request to database """

    # Ensure textfield isn't empty
    if not request.form.get("reason"):
        flash("Please specify what's wrong with the record")
        return redirect("/timesheet")


@app.route("/people", methods=["GET", "POST"])
@login_required
def colleagues():
    """ Querry for users of the same store

    Returns:
        list: colleagues information
    """

    # Fetch current user's assigned store.
    current_user = Users.query.filter_by(
                    id=session["user_id"]
                    ).first()

    # Group user by store id.
    people = Users.query.filter_by(
                    store_id=current_user.store_id
                    ).all()

    # Create a list of colleagues
    all_colleagues = []

    for person in people:
        all_colleagues.append(person)

    return render_template("people.html", all_colleagues=all_colleagues)

@app.route("/timeoff", methods=["GET", "POST"])
@login_required
def make_request():
    """ Querry all time off requests and save new requests """

    # Get all time off requests of user
    time_off = Timeoff.query.filter_by(
                    user_id=session["user_id"]).order_by(Timeoff.id.desc()
                    ).all()

    # Create a list of all requests
    t_off = []

    for data in time_off:
        t_off.append(data)

    if request.method == "POST":

        # Ensure date are inserted
        if not request.form.get("start") and not request.form.get("end"):
            flash("Please complete Dates")
            return redirect("/Timeoff")

        # Ensure text field is'nt empty
        if not request.form.get("reason"):
            flash("Please state reason")
            return redirect("/Timeoff")

        start = request.form.get("start").split("-")
        end = request.form.get("end").split("-")

        if not request.form.get("end"):
            end_date = start[2] + "/" + start[1] + "/" + start[0]
        else:
            end_date = end[2] + "/" + end[1] + "/" + end[0]

        # Commit time off request to DB
        new_timeoff = Timeoff(
                        user_id=session['user_id'], 
                        timestamp=str(datetime.datetime.now().strftime("%A, %d %B %Y at %H:%M")), 
                        from_off=start[2] + "/" + start[1] + "/" + start[0],
                        to_off=end_date, 
                        reason=request.form.get("reason"),
                        status='Pending')

        db.session.add(new_timeoff)
        db.session.commit()
        flash("Time-off request sent")
        
        return redirect("/timeoff")

    return render_template("timeoff.html", all_request=t_off)


@app.route("/timesheet", methods=["GET", "POST"])
@login_required
def sheet():
    """ Clock in / out history """
    
    # Query user's time sheet
    time_sheet = Timesheet.query.filter_by(
                    user_id=session["user_id"]
                    ).all()

    shifts = []
    shift_month = []

    if time_sheet:

        duplicates = ""

        for shift in time_sheet:
            if shift.month == str(now.month):
                shifts.append(shift)

            if shift.month != duplicates:
                val = {
                "name": calendar.month_name[int(shift.month)],
                "value" : shift.month
                }
                shift_month.append(val)
            
            duplicates = shift.month
            
    if request.method == "POST":
        
        current_month = calendar.month_name[int(request.form.get("month"))]

        # Query user's time sheet
        time_sheet = Timesheet.query.filter_by(
                        user_id=session["user_id"]
                        ).all()

        shifts = []
        shift_month = []

        if time_sheet:

            duplicates = ""

            for shift in time_sheet:
                if shift.month == str(request.form.get("month")):
                    shifts.append(shift)

                if shift.month != duplicates:
                    val = {
                    "name": calendar.month_name[int(shift.month)],
                    "value" : shift.month
                    }
                    shift_month.append(val)
                
                duplicates = shift.month

        return render_template("timesheet.html", 
                    all_shifts=shifts, 
                    month=current_month, 
                    shift_month=shift_month)

    return render_template("timesheet.html", 
                all_shifts=shifts, 
                month=calendar.month_name[datetime.datetime.now().month], 
                shift_month=shift_month)
    

@app.route("/clockout", methods=["GET", "POST"])
@login_required
def out():
    current_user = Users.query.filter_by(
                    id=session["user_id"]
                    ).first()

    face_path = os.path.join("static/faces/", current_user.face)
    
    last_clockin = Timesheet.query.filter_by(user_id=session["user_id"]
                        ).order_by(Timesheet.id.desc()
                        ).limit(1).first()

    if last_clockin.time_out != "Currently clocked in":
        return redirect("/")
            
    if request.method == "POST":
        current_user = Users.query.filter_by(id=session["user_id"]).first()

        
        # Get assigned position
        store = Stores.query.filter_by(
                    id=current_user.store_id
                    ).first()

        # Get current position
        try:
            assigned_position = [float(store.longitude), 
                                 float(store.latitude)]

            current_position = [float(request.form.get("long")), 
                                float(request.form.get("lat"))]
        except:
            status = False
            flash("Location not found. Turn on GPS on your phone settings and accept location service acces in your browser then try again.")
            return render_template("clockout.html", 
                        status=status, 
                        image=face_path, 
                        name=current_user.name)
        

        if distance(current_position, assigned_position) > radius:
            status = False
            flash("You are not within the perimeter")
            return render_template("clockout.html", 
                        status=status, 
                        image=face_path, 
                        name=current_user.username)

        last_clockin = Timesheet.query.filter_by(
                        user_id=session["user_id"]
                        ).order_by(Timesheet.id.desc()
                        ).limit(1).first()

        last_clockin.time_out = now.strftime("%H:%M")
        db.session.commit()

        status = True
        flash("Clocked-Out!")
        return redirect("/")

    return render_template("clockout.html", 
                image=face_path, 
                name=current_user.name, 
                hour=int(last_clockin.time_in[0:2]), 
                minute=int(last_clockin.time_in[3:5]))


@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    current_user = Users.query.filter_by(
                    id=session["user_id"]
                    ).first()

    face_path = os.path.join('static/faces/', current_user.face)
    
    try:
        last_clockin = Timesheet.query.filter_by(
                        user_id=session["user_id"]
                        ).order_by(Timesheet.id.desc()
                        ).limit(1).first()

        if last_clockin.time_out == "Currently clocked in":
            return redirect("/clockout")        
    except:
        pass

    if request.method == "POST":

        current_user = Users.query.filter_by(
                        id=session["user_id"]
                        ).first()

        if not current_user:
            flash("Error")
            return render_template("index.html")

        # Get assigned position
        store = Stores.query.filter_by(
                        id=current_user.store_id
                        ).first()

        # Query current user's position and assigned position
        try:
            assigned_position = [float(store.longitude), 
                                 float(store.latitude)]

            current_position = [float(request.form.get("long")), 
                                float(request.form.get("lat"))]
        except:
            flash("Location not found. Turn on GPS on your phone settings and accept location service acces in your browser then try again.")
            return render_template("index.html",
                        image=face_path, 
                        name=current_user.username)

        # Check if user is within the perimiter of the assigned position
        if distance(current_position, assigned_position) > radius:
            status = False
            flash("You are not within the perimeter")
            return render_template("index.html", 
                        status=status, 
                        image=face_path, 
                        name=current_user.username)

        # Record clock in to database
        new_clockin = Timesheet(user_id=session['user_id'], 
                                week=datetime.datetime.now().strftime("%A") ,
                                day=now.day, 
                                month=now.month, 
                                year=now.year,
                                time_in=now.strftime("%H:%M"), 
                                time_out="Currently clocked in")

        db.session.add(new_clockin)
        db.session.commit()

        # Flash success message
        flash("Clocked-In!")
        return redirect("/clockout")

    return render_template("index.html", 
                image=face_path, 
                name=current_user.name)


@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    """Register user"""

    all_stores = Stores.query.all()
    status = False

    # Get all time off requests of user
    time_off = Timeoff.query.all()

    # Create a list of all requests
    t_off = []

    for data in time_off:
        t_off.append(data)

    if request.method == "POST":

        # Get Form inputs
        name = request.form.get("name")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")

        # Check for non null input
        if not name and not lastname and not email:
            flash("Incomplete form")
            return redirect("/register")

        elif not password:
            flash("Incomplete form")
            return redirect("/register")

        elif not request.form.get("store") and not request.form.get("role"):
            flash("Incomplete form")
            return redirect("/register")

        # Check for password match
        elif password != request.form.get("confirmation"):
            flash("password not match", 400)
            return redirect("/register")

        # Check for image file
        if 'photo' not in request.files:
            flash('No file part')
            return redirect("/register")

        file = request.files['photo']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect("/register")

        # Ensure file is a secured file
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('static/faces/', filename))

        # Query store for coordinates from database
        store = Stores.query.filter_by(
                        name=request.form.get("store")
                        ).first()

        # Store registrants data to database
        new_user = Users(name=name, 
                         lastname=lastname, 
                         pw_hash=generate_password_hash(password), 
                         email=email, 
                         store_id=store.id,
                         face=filename, 
                         role=request.form.get("role"))

        # This operetion tries to commit new data to database
        # and avoids crash when username and email are already in use
        try:
            db.session.add(new_user)
            db.session.commit()
        except:
            status = False
            flash("Something went wrong. Try changing Username or E-mail address.", 400)
            return redirect("/register")

        flash("Successfully Registered")

        # Redirect user to log-in
        return redirect("/")

    return render_template("register.html",  
                stores=all_stores)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        email = request.form.get("email")

        # Ensure username was submitted
        if not email:
            flash("Must Provide E-mail address")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must Provide Password", 400)
            return render_template("login.html")

        # Query database for username
        user = Users.query.filter_by(
                        email=email
                        ).first()

        # Check username validity
        if user == None:
            flash("invalid E-mail address and/or password", 403)
            return render_template("login.html")

        # Check Password validity
        if not check_password_hash(user.pw_hash, request.form.get("password")):
            flash("invalid username and/or password", 403)
            return render_template("login.html") 

        # # Remember which user has logged in
        session["user_id"] = user.id

        if request.form.get("remember"):
            session.permanent = True

        global access_type
        access_type = user.role

        global user_name
        user_name = user.name + ' ' + user.lastname

        global image_path
        image_path = os.path.join('static/faces/', user.face)
        
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


if __name__ == "__main__":
    app.run(ssl_context='adhoc')